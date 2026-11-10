from html import unescape
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from urllib.request import urlopen


MAX_PAGE_BYTES = 1_000_000


class FileAndWebRepository:
    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8-sig")

    def read_page(self, url: str) -> str:
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ValueError("Укажи URL с http:// или https://")
        with urlopen(url, timeout=10) as response:
            content = response.read(MAX_PAGE_BYTES + 1)
            charset = response.headers.get_content_charset() or "utf-8"
            is_html = response.headers.get_content_type() == "text/html"
        if len(content) > MAX_PAGE_BYTES:
            raise ValueError("Страница больше 1 МБ")
        text = content.decode(charset, errors="replace")
        return unescape(text) if is_html else text

    def write(self, path: Path, addresses: list[str]):
        with TemporaryDirectory(dir=path.parent) as folder:
            temporary = Path(folder) / path.name
            text = "\n".join(addresses) + "\n"
            temporary.write_text(text, encoding="utf-8", newline="\n")
            temporary.replace(path)
