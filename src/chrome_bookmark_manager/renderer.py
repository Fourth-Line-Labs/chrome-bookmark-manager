from __future__ import annotations

from typing import TYPE_CHECKING

from chrome_bookmark_manager.models import (
    BookmarkNode,
    ChromeBookmarksFile,
    ChromeFolderNode,
    ChromeUrlNode,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


def render_markdown(bookmarks: ChromeBookmarksFile) -> str:
    lines = ["# Chrome Bookmarks", ""]
    for root in _iter_roots(bookmarks):
        lines.append(f"## {_escape_text(root.name)}")
        if root.children:
            lines.extend(_render_nodes(root.children, depth=0))
        else:
            lines.append("- (empty)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _iter_roots(bookmarks: ChromeBookmarksFile) -> Iterable[ChromeFolderNode]:
    roots = bookmarks.roots
    for root in (roots.bookmark_bar, roots.other, roots.synced):
        if root is not None:
            yield root


def _render_nodes(nodes: Iterable[BookmarkNode], *, depth: int) -> list[str]:
    lines: list[str] = []
    indent = "  " * depth
    for node in nodes:
        if isinstance(node, ChromeUrlNode):
            lines.append(f"{indent}- [{_escape_link_label(node.name)}]({node.url})")
            continue

        lines.append(f"{indent}- {_escape_text(node.name)}")
        lines.extend(_render_nodes(node.children, depth=depth + 1))
    return lines


def _escape_text(value: str) -> str:
    return value.replace("\n", " ").strip()


def _escape_link_label(value: str) -> str:
    return _escape_text(value).replace("[", r"\[").replace("]", r"\]")
