from django.apps import AppConfig

class MailingsConfig(AppConfig):
    """
    Конфигурация приложения Mailings.

    Этот класс настраивает приложение Mailings и запускает планировщик задач при готовности приложения.
    """

    name = 'mailings'

    def ready(self):
        """
        Метод, вызываемый при готовности приложения.

        Запускает планировщик задач, который будет выполнять запланированные задачи.
        """
        from .tasks import start_scheduler
        start_scheduler()
