import re
from pathlib import Path


ATOM_CHARS = r"A-Za-z0-9!#$%&'*+/=?^_`{|}~\-"
DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
EMAIL_RE = re.compile(
    rf"[{ATOM_CHARS}]+(?:\.[{ATOM_CHARS}]+)*"
    rf"@(?:{DOMAIN_LABEL}\.)+[A-Za-z]{{2,63}}"
)
CANDIDATE_RE = re.compile(
    rf"(?<![\w{ATOM_CHARS}.@])[{ATOM_CHARS}.]+@[\w.-]+(?![\w.@-])"
)


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


def main():
    while True:
        print("\n1. Проверить e-mail  2. Поиск в тексте")
        print("3. Поиск в файле  0. Выход")
        choice = input("Действие: ").strip()
        if choice == "0":
            return
        if choice == "1":
            address = input("E-mail: ")
            print("Адрес корректный" if is_email(address)
                  else "Адрес некорректный")
        elif choice == "2":
            show_results(find_emails(input("Текст: ")))
        elif choice == "3":
            path = Path(input("Путь к файлу: ").strip())
            try:
                text = path.read_text(encoding="utf-8-sig")
                show_results(find_emails(text))
            except (OSError, UnicodeError) as error:
                print(f"Ошибка чтения: {error}")
        else:
            print("Выбери действие из меню")


if __name__ == "__main__":
    main()
