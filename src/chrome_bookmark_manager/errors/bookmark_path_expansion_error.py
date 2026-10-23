from chrome_bookmark_manager.errors.bookmark_parse_error import BookmarkParseError


class BookmarkPathExpansionError(BookmarkParseError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Cannot expand '~' in bookmark path: {path}")
