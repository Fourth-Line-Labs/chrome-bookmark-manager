import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import LATEST_PROTOCOL_VERSION, TextContent

from chrome_bookmark_manager import __version__
from chrome_bookmark_manager.discovery import candidate_bookmark_paths, current_platform
from chrome_bookmark_manager.logging_setup import LOG_DIR_ENV_VAR, LOG_FILE_NAME
from chrome_bookmark_manager.mcp_server import (
    build_server,
    get_bookmark_tree,
    get_bookmarks_markdown,
)

FIXTURES = Path(__file__).parent / "fixtures" / "bookmarks"
SIMPLE = FIXTURES / "simple_bookmarks.json"
MALFORMED_CANARY = "Canary Bookmark Name"
TOOL_NAMES = {"list_bookmark_files", "get_bookmark_tree", "get_bookmarks_markdown"}
SUBPROCESS_TIMEOUT_SECONDS = 30
SERVER_COMMAND = "chrome-bookmark-manager-mcp"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def test_get_bookmark_tree_returns_parsed_file() -> None:
    bookmarks = get_bookmark_tree(str(SIMPLE))

    assert bookmarks.roots.bookmark_bar is not None
    assert bookmarks.roots.bookmark_bar.name == "Bookmarks Bar"


def test_get_bookmarks_markdown_renders_outline() -> None:
    markdown = get_bookmarks_markdown(str(SIMPLE))

    assert "- [Python](https://www.python.org/)" in markdown


def test_tools_expand_home_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    shutil.copy(SIMPLE, tmp_path / "Bookmarks")

    markdown = get_bookmarks_markdown("~/Bookmarks")

    assert "- [Python](https://www.python.org/)" in markdown


def test_missing_file_becomes_tool_error(tmp_path: Path) -> None:
    with pytest.raises(ToolError, match="does not exist"):
        get_bookmark_tree(str(tmp_path / "Bookmarks"))


def test_tool_error_does_not_echo_bookmark_content() -> None:
    with pytest.raises(ToolError) as excinfo:
        get_bookmark_tree(str(FIXTURES / "malformed.json"))

    assert MALFORMED_CANARY not in str(excinfo.value)


@pytest.mark.anyio
async def test_server_registers_read_only_tools() -> None:
    tools = await build_server().list_tools()

    assert {tool.name for tool in tools} == TOOL_NAMES
    for tool in tools:
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is True
        assert tool.annotations.destructiveHint is False
        assert tool.outputSchema is not None


def _server_env(log_dir: Path, home: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env[LOG_DIR_ENV_VAR] = str(log_dir)
    if home is not None:
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env["LOCALAPPDATA"] = str(home / "AppData" / "Local")
    return env


def _server_command() -> str:
    """Find the installed entry point next to the running interpreter."""
    command = shutil.which(SERVER_COMMAND, path=str(Path(sys.executable).parent))
    assert command is not None, f"{SERVER_COMMAND} is not installed; run poetry install"
    return command


def _server_params(env: dict[str, str]) -> StdioServerParameters:
    return StdioServerParameters(command=_server_command(), env=env)


@pytest.mark.anyio
async def test_stdio_server_serves_bookmark_tree(isolated_log_dir: Path) -> None:
    params = _server_params(_server_env(isolated_log_dir))

    async with (
        stdio_client(params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        tree = await session.call_tool("get_bookmark_tree", {"path": str(SIMPLE)})
        markdown = await session.call_tool(
            "get_bookmarks_markdown",
            {"path": str(SIMPLE)},
        )

    assert not tree.isError
    assert tree.structuredContent is not None
    assert tree.structuredContent["roots"]["bookmark_bar"]["name"] == "Bookmarks Bar"
    assert not markdown.isError
    assert markdown.structuredContent is not None
    assert "- [Python](https://www.python.org/)" in markdown.structuredContent["result"]

    log = (isolated_log_dir / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert f"chrome-bookmark-manager MCP server {__version__} starting" in log
    assert f"Tool get_bookmark_tree called for {SIMPLE}" in log


@pytest.mark.anyio
async def test_stdio_server_reports_parse_errors_as_tool_errors(
    tmp_path: Path,
    isolated_log_dir: Path,
) -> None:
    params = _server_params(_server_env(isolated_log_dir))

    async with (
        stdio_client(params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        result = await session.call_tool(
            "get_bookmark_tree",
            {"path": str(tmp_path / "Bookmarks")},
        )

    assert result.isError
    messages = [
        block.text for block in result.content if isinstance(block, TextContent)
    ]
    assert any("does not exist" in message for message in messages)


@pytest.mark.anyio
async def test_stdio_server_lists_discovered_files(
    tmp_path: Path,
    isolated_log_dir: Path,
) -> None:
    home = tmp_path / "home"
    env = _server_env(isolated_log_dir, home)
    expected = candidate_bookmark_paths(
        platform=current_platform(),
        home=home,
        env=env,
    )[0]
    bookmarks_file = Path(expected.path)
    bookmarks_file.parent.mkdir(parents=True)
    shutil.copy(SIMPLE, bookmarks_file)

    async with (
        stdio_client(_server_params(env)) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        result = await session.call_tool("list_bookmark_files", {})

    assert not result.isError
    assert result.structuredContent == {
        "result": [
            {
                "browser": expected.browser,
                "profile": expected.profile,
                "path": str(expected.path),
            },
        ],
    }


def test_stdout_carries_only_protocol_messages(isolated_log_dir: Path) -> None:
    """Under stdio, any stray stdout write would corrupt the MCP session."""
    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": LATEST_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "stdout-test", "version": "0"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "get_bookmark_tree", "arguments": {"path": str(SIMPLE)}},
        },
    ]
    stdin = "".join(json.dumps(message) + "\n" for message in messages)
    # Unbuffered, so a stray write reaches stdout at once. Buffered, it could
    # sit unflushed until the SDK closes stdout at exit and silently vanish.
    env = _server_env(isolated_log_dir)
    env["PYTHONUNBUFFERED"] = "1"

    completed = subprocess.run(  # noqa: S603 - fixed argv, our own installed entry point
        [_server_command(), "-vv"],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=SUBPROCESS_TIMEOUT_SECONDS,
        check=False,
    )

    lines = completed.stdout.splitlines()
    assert lines, completed.stderr
    responses = [json.loads(line) for line in lines]
    assert all(response["jsonrpc"] == "2.0" for response in responses)
    assert {response["id"] for response in responses} == {1, 2}
    assert "MCP server" in completed.stderr
