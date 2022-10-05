from mail_sender.celery import app
from django.db.models import F, Q
from django.utils import timezone
from django.db import transaction, DatabaseError
from .email_sender.abstract_email_sender import AbstractEmailSender
from .email_sender.mailjet_email_sender import MailjetEmailWrapper
from django.conf import settings
from .services import EmailService
from .constants import *
from .exceptions import EmailSendingFailedWith429or500


@app.task(bind=True, max_retries=3)
def send_email(self, email_scheduler_obj_id, retry_count=0):

    try:
        EmailService.send_email(
            email_scheduler_obj_id=email_scheduler_obj_id,
            max_retries=self.max_retries,
            retry_count=retry_count,
        )
    except EmailSendingFailedWith429or500:
        self.retry(kwargs={"retry_count": retry_count + 1}, countdown=30)
