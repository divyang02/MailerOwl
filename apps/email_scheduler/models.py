from django.db import models
from django.contrib.postgres.fields import ArrayField
from .constants import *
from django.utils import timezone
from django.db.models import F, Q

# Create your models here.


class EmailScheduler(models.Model):
    email_to = models.EmailField()
    email_cc = ArrayField(
        models.EmailField(),
        blank=True,
        default=list,
        help_text="list of comma separated email address in Cc",
    )
    email_bcc = ArrayField(
        models.EmailField(),
        blank=True,
        default=list,
        help_text="list of comma separated email address in Bcc",
    )
    email_subject = models.CharField(max_length=256)
    email_body = models.TextField()

    email_schedule = models.DateTimeField(
        blank=True, null=True, help_text="Schedule time to send email"
    )
    email_repeat_after = models.DurationField(
        blank=True,
        null=True,
        help_text="Duration after which to resend email, You can remove it in future to stop the campaign and mark "
        "the task COMPLETE",
    )

    email_service = models.CharField(
        max_length=32, default=DEFAULT_EMAIL_SERVICE, choices=EMAIL_SERVICE_CHOICES
    )

    email_last_sent_at = models.DateTimeField(blank=True, null=True)
    task_status = models.CharField(
        default=TASK_STATUS_PENDING,
        choices=TASK_STATUS_CHOICES,
        max_length=128,
        help_text="Status of this email sending task",
    )
    email_send_count = models.IntegerField(
        default=0, help_text="Count of emails sent successfully"
    )
    task_failed_count = models.IntegerField(
        default=0, help_text="Count of number of times this task failed"
    )
    task_failure_info = ArrayField(
        models.JSONField(),
        null=True,
        blank=True,
        help_text="If task failed, information regarding why it failed",
    )


class EmailSchedulerLogs(models.Model):
    email_scheduler = models.ForeignKey(EmailScheduler, on_delete=models.CASCADE)
    email_recipient_id = models.EmailField()
    email_message_id = models.TextField(null=True, blank=True)
    email_send_status = models.CharField(max_length=128, blank=True, null=True)
    email_recipient_type = models.CharField(
        max_length=8, choices=EMAIL_RECIPIENT_TYPE_CHOICES
    )
    retry_count = models.IntegerField(
        default=0, help_text="Number of times this email is being retried"
    )
    email_event_info = models.JSONField(null=True, blank=True)