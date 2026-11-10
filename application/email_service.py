from pathlib import Path

from domain.email import CANDIDATE_RE, is_email
from domain.repository import TextRepository


def find_emails(text: str) -> list[str]:
    addresses: dict[str, bool] = {}
    for match in CANDIDATE_RE.finditer(text):
        address = match.group().removesuffix(".")
        if is_email(address):
            local, domain = address.split("@")
            addresses[f"{local}@{domain.lower()}"] = True
    return list(addresses)


class EmailService:
    def __init__(self, repository: TextRepository):
        self.repository = repository

    def check(self, address: str) -> bool:
        return is_email(address)

    def search(self, value: str, source: str = "text") -> list[str]:
        if source == "file":
            value = self.repository.read_file(Path(value.strip()))
        elif source == "url":
            value = self.repository.read_page(value.strip())
        return find_emails(value)

    def save(self, path: Path, addresses: list[str]):
        self.repository.write(path, addresses)
