from django.db import models
from django.contrib.postgres.fields import ArrayField
from .tasks import send_email
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

    @classmethod
    def pending_periodic_email_finder(cls):
        """This method finds all the EmailScheduler objects which need to be sent in case of periodic task"""

        pending_emails = (
            cls.objects.select_for_update()
            .exclude(email_repeat_after__exact=None, email_last_sent_at__exact=None)
            .filter(
                task_status__exact=TASK_STATUS_PENDING,
                email_last_sent_at__lte=timezone.now() - F("email_repeat_after"),
            )
        )
        return pending_emails

    def pre_update_processing(self):
        """
        The purpose of this method is, to do preprocessing before updating an object.
        Currently, when we are updating an EmailScheduler object, and we are changing
        the email_repeat_after to None then we should automatically mark the task complete
        if it's not already in Failed state. Here we first fetch the object from db which contains the old state
        before updating and self contains the state after updating, hence db call is necessary.
        """
        old_obj = EmailScheduler.objects.get(pk=self.pk)
        if (
            old_obj.email_repeat_after is not None
            and self.email_repeat_after is None
            and old_obj.task_status != TASK_STATUS_FAILED
        ):
            self.task_status = TASK_STATUS_COMPLETE

    def save(self, *args, **kwargs):
        """
        We have overrided the save method to call respective send email method i.e send immidiately or
        after specified duration. We also call pre_update_processing to update the obejct properly in case of
        update.
        """
        is_adding_new = self._state.adding
        if not is_adding_new:
            self.pre_update_processing()
        super(EmailScheduler, self).save(*args, **kwargs)
        if is_adding_new:
            if self.email_schedule is None:
                send_email.delay(self.pk)
            elif self.email_schedule is not None:
                td = self.email_schedule
                send_email.apply_async(
                    kwargs={"email_scheduler_obj_id": self.pk}, eta=td
                )

    def update_fields(self, updated_fields: dict):
        """
        This method takes the dict of the updated keys in the model. It updates the
        corresponding fields in the model instance and saves it in db.
        """
        update_fields = []
        for key, value in updated_fields.items():
            setattr(self, key, value)
            update_fields.append(key)
        self.save(update_fields=update_fields)



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