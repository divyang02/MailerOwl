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

@app.task
def periodic_email_sender():
    """
    This method is used to send emails periodically
    """
    from .models import EmailScheduler

    queryset = EmailScheduler.pending_periodic_email_finder()
    """
    We are using atomic transaction here as the queryset returned has been fetched using select_for_update
    which requires an atomic transaction in order to evaluate that queryset.
    """
    try:
        with transaction.atomic():
            for email_scheduler in queryset:
                send_email(email_scheduler.pk)
    except DatabaseError:
        pass


@app.task
def periodic_email_log_updater():
    """
    This method is used to update the logs of periodic emails
    """
    EmailService.email_scheduler_log_updater()

@app.task(bind=True, max_retries=3)
def send_email(self, email_scheduler_obj_id, retry_count=0):
    """
    This method is used to send email
    Arguments:
        email_scheduler_obj_id {int} -- Email scheduler object id
        retry_count {int} -- Retry count
    """

    try:
        EmailService.send_email(
            email_scheduler_obj_id=email_scheduler_obj_id,
            max_retries=self.max_retries,
            retry_count=retry_count,
        )
    except EmailSendingFailedWith429or500:
        self.retry(kwargs={"retry_count": retry_count + 1}, countdown=30)
