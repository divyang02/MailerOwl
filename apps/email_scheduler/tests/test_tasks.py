from django.test import TestCase
from mock import patch
from ..models import EmailScheduler, EmailSchedulerLogs
from ..tasks import send_email, periodic_email_sender, periodic_email_log_updater
from time import sleep
from django.utils import timezone
from ..constants import TASK_STATUS_PENDING
from ..exceptions import EmailSendingFailedWith429or500


class TestTasks(TestCase):

    @patch("apps.email_scheduler.services.EmailService.send_email")
    @patch("apps.email_scheduler.tasks.send_email.retry")
    def test_send_email_failed_with_retry(self, mock_retry,
                                          mock_email_send_service):
        mock_email_send_service.side_effect = EmailSendingFailedWith429or500()

        email_scheduler_err = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="test")

        send_email(email_scheduler_err.pk)
        mock_retry.assert_called_with(kwargs={"retry_count": 1}, countdown=30)
        email_scheduler_err.refresh_from_db()
        self.assertEqual(email_scheduler_err.task_status, TASK_STATUS_PENDING)

    @patch("apps.email_scheduler.tasks.send_email")
    def test_periodic_email_sender(self, mock_send_email):
        periodic_email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="test",
            email_repeat_after=timezone.timedelta(seconds=1),
            email_last_sent_at=timezone.now(),
        )
        sleep(1)
        periodic_email_sender()
        mock_send_email.assert_called_once_with(periodic_email_scheduler.pk)

    @patch(
        "apps.email_scheduler.services.EmailService.email_scheduler_log_updater"
    )
    def test_periodic_email_log_updater(self,
                                        mock_email_scheduler_log_updater):
        periodic_email_log_updater()
        mock_email_scheduler_log_updater.assert_called_once()
