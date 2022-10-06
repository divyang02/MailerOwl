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

    def test_update_repeat_to_none_marks_task_complete(self):
        with patch("apps.email_scheduler.models.send_email.delay") as mock_task:
            email_scheduler_new = EmailScheduler.objects.create(
                email_to="abc@gmail.com",
                email_subject="Test subject 2 ",
                email_body="Test email body 2",
                email_repeat_after=timezone.timedelta(minutes=1),
            )
            email_scheduler_new.email_repeat_after = None
            email_scheduler_new.save()
            email_scheduler_new.refresh_from_db()
            self.assertEqual(email_scheduler_new.email_repeat_after, None)
            self.assertEqual(email_scheduler_new.task_status, TASK_STATUS_COMPLETE)

    def test_updating_failed_task_does_not_complete(self):
        with patch("apps.email_scheduler.models.send_email.delay") as mock_task:
            email_scheduler_new = EmailScheduler.objects.create(
                email_to="abc@gmail.com",
                email_subject="Test subject 2 ",
                email_body="Test email body 2",
                email_repeat_after=timezone.timedelta(minutes=1),
                task_status=TASK_STATUS_FAILED,
            )
            email_scheduler_new.email_repeat_after = None
            email_scheduler_new.save()
            email_scheduler_new.refresh_from_db()
            self.assertEqual(email_scheduler_new.email_repeat_after, None)
            self.assertNotEqual(email_scheduler_new.task_status, TASK_STATUS_COMPLETE)

    def test_pending_email_finder(self):
        periodic_email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="test",
            email_repeat_after=timezone.timedelta(seconds=1),
            email_last_sent_at=timezone.now(),
        )
        sleep(1)
        queryset = EmailScheduler.pending_periodic_email_finder()
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].pk, periodic_email_scheduler.pk)

    def test_email_scheduler_updater(self):
        email_scheduler_to_be_updated = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="test",
            email_repeat_after=timezone.timedelta(seconds=1),
            email_last_sent_at=timezone.now(),
        )
        email_scheduler_to_be_updated.update_fields({"email_send_count": 1})
        email_scheduler_to_be_updated.refresh_from_db()
        self.assertEqual(email_scheduler_to_be_updated.email_send_count, 1)

class TestEmailSchedulerLogsModel(TestCase):
    def test_create_logs(self):
        email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="Test email body 2",
        )
        log_list = [
            {
                "email_scheduler": email_scheduler,
                "email_recipient_id": "abc@gmail.com",
                "email_message_id": "1",
                "email_recipient_type": EMAIL_RECIPIENT_TYPE_TO,
            }
        ]
        EmailSchedulerLogs.create_logs(log_list)
        self.assertEqual(len(EmailSchedulerLogs.objects.all()), 1)
        self.assertEqual(EmailSchedulerLogs.objects.all()[0].email_message_id, "1")

    def test_get_logs_to_be_updated(self):
        email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="Test email body 2",
        )
        email_scheduler_log = EmailSchedulerLogs.objects.create(
            email_scheduler=email_scheduler,
            email_recipient_id="abc@gmail.com",
            email_message_id="1",
            email_recipient_type=EMAIL_RECIPIENT_TYPE_TO,
        )

        queryset = EmailSchedulerLogs.get_logs_to_be_updated()
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].email_message_id, "1")

    def test_email_scheduler_logs_updater(self):
        email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="test",
        )
        email_scheduler_log_to_be_updated = EmailSchedulerLogs.objects.create(
            email_scheduler=email_scheduler,
            email_recipient_id="abc@gmail.com",
            email_message_id="1",
            email_recipient_type=EMAIL_RECIPIENT_TYPE_TO,
        )
        email_scheduler_log_to_be_updated.update_fields({"email_send_status": "sent"})
        email_scheduler_log_to_be_updated.refresh_from_db()
        self.assertEqual(email_scheduler_log_to_be_updated.email_send_status, "sent")