from django.test import TestCase
from ..models import EmailScheduler, EmailSchedulerLogs
from mock import patch
from django.utils import timezone
from ..constants import (
    TASK_STATUS_COMPLETE,
    TASK_STATUS_FAILED,
    EMAIL_RECIPIENT_TYPE_TO,
)
from time import sleep


class TestEmailSchedulerModel(TestCase):
    def test_direct_email_send_task_called(self):
        with patch("apps.email_scheduler.models.send_email.delay") as mock_task:
            email_scheduler_new = EmailScheduler.objects.create(
                email_to="abc@gmail.com",
                email_subject="Test subject 2 ",
                email_body="Test email body 2",
            )
            mock_task.assert_called_once_with(email_scheduler_new.pk)

    def test_scheduled_email_send_task_called(self):
        with patch("apps.email_scheduler.models.send_email.apply_async") as mock_task:
            email_scheduler_new = EmailScheduler.objects.create(
                email_to="abc@gmail.com",
                email_subject="Test subject 3",
                email_body="Test email body 3",
                email_schedule=timezone.now() + timezone.timedelta(minutes=1),
            )
            mock_task.assert_called_once_with(
                kwargs={"email_scheduler_obj_id": email_scheduler_new.pk},
                eta=email_scheduler_new.email_schedule,
            )