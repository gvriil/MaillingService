from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Attempt


def send_mail(subject, body, recipient_list, request_user, mailing=None):
    email_body = render_to_string(
        "mailings/email_template.html",
        {
            "subject": subject,
            "body": body,
            "site_name": "Ваш сервис рассылок",
        },
    )

    try:
        email = EmailMessage(
            subject, email_body, settings.DEFAULT_FROM_EMAIL, recipient_list
        )
        email.content_subtype = "html"
        email.send()

        Attempt.objects.create(
            mailing=mailing,
            status="success",
            server_response="Email успешно отправлен.",
            owner=request_user,
        )
        return True, "Письмо успешно отправлено."

    except Exception as e:
        Attempt.objects.create(
            mailing=mailing,
            status="failed",
            server_response=str(e),
            owner=request_user,
        )
        return False, str(e)
