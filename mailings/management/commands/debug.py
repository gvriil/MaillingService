from django.core.management import BaseCommand
from mailings.tasks import send_mails


class Command(BaseCommand):
    """
    Пользовательская команда Django для запуска задачи отправки рассылок.

    Эта команда вызывает функцию `send_mails` из модуля `mailings.tasks`,
    которая отвечает за отправку всех запланированных рассылок.
    """

    def handle(self, *args, **options):
        """
        Основной метод, который выполняется при вызове команды.

        Args:
            *args: Дополнительные аргументы.
            **options: Дополнительные опции.
        """
        send_mails()
