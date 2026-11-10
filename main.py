import re


ATOM_CHARS = r"A-Za-z0-9!#$%&'*+/=?^_`{|}~-"
DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
EMAIL_RE = re.compile(
    rf"[{ATOM_CHARS}]+(?:\.[{ATOM_CHARS}]+)*"
    rf"@(?:{DOMAIN_LABEL}\.)+[A-Za-z]{{2,63}}"
)


def is_email(value: str) -> bool:
    address = value.strip()
    local = address.split("@", 1)[0]
    return (
        len(address) <= 254
        and len(local) <= 64
        and EMAIL_RE.fullmatch(address) is not None
    )


def main():
    address = input("E-mail: ")
    print("Адрес корректный" if is_email(address) else "Адрес некорректный")


if __name__ == "__main__":
    main()
