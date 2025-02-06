from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from .models import Mailing, Attempt
from .services import send_mail

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def send_scheduled_mailings():
    """Функция для отправки запланированных рассылок."""
    mailings = Mailing.objects.filter(
        status="running",
        start_datetime__lte=timezone.now(),
        end_datetime__gte=timezone.now(),
    )
    for mailing in mailings:
        message = mailing.message  # Получаем связанное сообщение
        subject = message.subject
        body = message.body
        recipient_list = [client.email for client in mailing.clients.all()]
        success, response = send_mail(
            subject=subject,
            body=body,
            recipient_list=recipient_list,
            request_user=mailing.owner,
            mailing=mailing,
        )
        if success:
            Attempt.objects.create(
                mailing=mailing,
                status="success",
                server_response=response,
                owner=mailing.owner,
            )
        else:
            Attempt.objects.create(
                mailing=mailing,
                status="failed",
                server_response=response,
                owner=mailing.owner,
            )

def start_scheduler():
    """Запускает планировщик задач."""
    if not scheduler.running:
        scheduler.add_job(
            send_scheduled_mailings,
            "interval",
            minutes=1,
            id="send_mailings",
            replace_existing=True,
        )
        scheduler.start()
