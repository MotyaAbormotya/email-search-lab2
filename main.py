from application.email_service import EmailService, find_emails as find_emails
from domain.email import is_email as is_email
from infrastructure.text_repository import FileAndWebRepository
from presentation.console import run


def main():
    repository = FileAndWebRepository()
    service = EmailService(repository)
    run(service)


if __name__ == "__main__":
    main()
