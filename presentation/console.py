from http.client import HTTPException
from pathlib import Path

from application.email_service import EmailService


SOURCES = {
    "2": ("text", "Текст: "),
    "3": ("file", "Путь к файлу: "),
    "4": ("url", "URL: "),
}


def run(service: EmailService):
    while True:
        print("\n1. Проверить e-mail  2. Поиск в тексте")
        print("3. Поиск в файле  4. Поиск по URL  0. Выход")
        try:
            choice = input("Действие: ").strip()
            if choice == "0":
                return
            if choice == "1":
                address = input("E-mail: ")
                print("Адрес корректный" if service.check(address)
                      else "Адрес некорректный")
                continue
            if choice not in SOURCES:
                print("Выбери действие из меню")
                continue
            source, prompt = SOURCES[choice]
            addresses = service.search(input(prompt), source)
            print(f"Найдено: {len(addresses)}", *addresses, sep="\n")
            if addresses and (
                input("Сохранить? (д/н): ").strip().lower() == "д"
            ):
                path = Path(input("Имя файла: ").strip())
                service.save(path, addresses)
                print(f"Сохранено: {path}")
        except (OSError, ValueError, LookupError, HTTPException) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход")
            return
