from pathlib import Path

from chrome_bookmark_manager.parser import load_bookmarks_file
from chrome_bookmark_manager.renderer import render_markdown

FIXTURES = Path(__file__).parent / "fixtures" / "bookmarks"


def test_renders_roots_and_url_links() -> None:
    bookmarks = load_bookmarks_file(FIXTURES / "simple_bookmarks.json")

    markdown = render_markdown(bookmarks)

    assert "# Chrome Bookmarks" in markdown
    assert "## Bookmarks Bar" in markdown
    assert "- [Python](https://www.python.org/)" in markdown
    assert "## Other Bookmarks" in markdown
    assert "## Mobile Bookmarks" in markdown


def test_renders_nested_folders_with_indentation() -> None:
    bookmarks = load_bookmarks_file(FIXTURES / "nested_bookmarks.json")

    markdown = render_markdown(bookmarks)

    assert "- Engineering" in markdown
    assert "  - References" in markdown
    assert "    - [Python Docs](https://docs.python.org/3/)" in markdown
