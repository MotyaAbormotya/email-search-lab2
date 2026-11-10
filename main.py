import re
from html import unescape
from http.client import HTTPException
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from urllib.request import urlopen


ATOM_CHARS = r"A-Za-z0-9!#$%&'*+/=?^_`{|}~\-"
DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
EMAIL_RE = re.compile(
    rf"[{ATOM_CHARS}]+(?:\.[{ATOM_CHARS}]+)*"
    rf"@(?:{DOMAIN_LABEL}\.)+[A-Za-z]{{2,63}}"
)
CANDIDATE_RE = re.compile(
    rf"(?<![\w{ATOM_CHARS}.@])[{ATOM_CHARS}.]+@[\w.-]+(?![\w.@-])"
)
MAX_PAGE_BYTES = 1_000_000


def is_email(value: str) -> bool:
    address = value.strip()
    local = address.split("@", 1)[0]
    return (
        len(address) <= 254
        and len(local) <= 64
        and EMAIL_RE.fullmatch(address) is not None
    )


def find_emails(text: str) -> list[str]:
    addresses: dict[str, bool] = {}
    for match in CANDIDATE_RE.finditer(text):
        address = match.group().removesuffix(".")
        if is_email(address):
            local, domain = address.split("@")
            addresses[f"{local}@{domain.lower()}"] = True
    return list(addresses)


def show_results(addresses: list[str]):
    print(f"Найдено: {len(addresses)}")
    for address in addresses:
        print(address)


def read_page(url: str) -> str:
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


def save_results(path: Path, addresses: list[str]):
    with TemporaryDirectory(dir=path.parent) as folder:
        temporary = Path(folder) / path.name
        text = "\n".join(addresses) + "\n"
        temporary.write_text(text, encoding="utf-8", newline="\n")
        temporary.replace(path)


def main():
    while True:
        print("\n1. Проверить e-mail  2. Поиск в тексте")
        print("3. Поиск в файле  4. Поиск по URL  0. Выход")
        try:
            choice = input("Действие: ").strip()
            if choice == "0":
                return
            if choice == "1":
                address = input("E-mail: ")
                print("Адрес корректный" if is_email(address)
                      else "Адрес некорректный")
                continue
            if choice == "2":
                text = input("Текст: ")
            elif choice == "3":
                path = Path(input("Путь к файлу: ").strip())
                text = path.read_text(encoding="utf-8-sig")
            elif choice == "4":
                text = read_page(input("URL: ").strip())
            else:
                print("Выбери действие из меню")
                continue
            addresses = find_emails(text)
            show_results(addresses)
            if addresses and (
                input("Сохранить? (д/н): ").strip().lower() == "д"
            ):
                path = Path(input("Имя файла: ").strip())
                save_results(path, addresses)
                print(f"Сохранено: {path}")
        except (OSError, ValueError, LookupError, HTTPException) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход")
            return


if __name__ == "__main__":
    main()
