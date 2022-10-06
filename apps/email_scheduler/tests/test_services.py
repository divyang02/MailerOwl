from django.test import TestCase
from mock import patch
from ..models import EmailScheduler, EmailSchedulerLogs
from ..services import EmailService
from time import sleep
from django.utils import timezone
from ..constants import *
from ..exceptions import EmailSendingFailedWith429or500


class TestService(TestCase):
    def setUp(self):
        self.mock_mailjet_return_value = {
            "Messages": [
                {
                    "Status": "success",
                    "CustomID": "",
                    "To": [
                        {
                            "Email": "abc@gmail.com",
                            "MessageUUID": "1",
                            "MessageID": 1,
                            "MessageHref": "https://api.mailjet.com/v3/REST/message/288230382216082166",
                        }
                    ],
                    "Cc": [],
                    "Bcc": [],
                }
            ]
        }
        self.email_scheduler = EmailScheduler.objects.create(
            email_to="abc@gmail.com",
            email_subject="Test subject 2 ",
            email_body="Test email body 2",
        )

    def test_send_email_called_with_proper_obj(self):
        with patch(
            "apps.email_scheduler.email_sender.MailjetEmailWrapper.send_email_with_service"
        ) as mock_mailjet_email_sender:
            mock_mailjet_email_sender.return_value = self.mock_mailjet_return_value
            EmailService.send_email(
                email_scheduler_obj_id=self.email_scheduler.pk,
                max_retries=3,
                retry_count=0,
            )
            mock_mailjet_email_sender.assert_called_once_with(self.email_scheduler)

    def test_send_email_success(self):
        with patch(
            "apps.email_scheduler.email_sender.MailjetEmailWrapper.send_email_with_service"
        ) as mock_mailjet_email_sender:
            mock_mailjet_email_sender.return_value = self.mock_mailjet_return_value
            EmailService.send_email(
                email_scheduler_obj_id=self.email_scheduler.pk,
                max_retries=3,
                retry_count=0,
            )
            email_scheduler_log_created = EmailSchedulerLogs.objects.filter(
                email_scheduler=self.email_scheduler
            )[0]

            self.assertIsNotNone(email_scheduler_log_created)
            self.assertEqual(email_scheduler_log_created.email_message_id, "1")
            self.email_scheduler.refresh_from_db()
            self.assertEqual(self.email_scheduler.task_status, TASK_STATUS_COMPLETE)

    def test_send_email_failed_without_retry(self):
        with patch(
            "apps.email_scheduler.email_sender.MailjetEmailWrapper.send_email_with_service"
        ) as mock_mailjet_email_sender:
            mock_mailjet_email_sender.return_value = {
                "Messages": [
                    {
                        "Status": "error",
                        "Errors": [
                            {
                                "ErrorIdentifier": "21e28b7d-cf57-4178-8481-d9589f84c6c3",
                                "ErrorCode": "send-0003",
                                "StatusCode": 400,
                                "ErrorMessage": 'At least "HTMLPart", "TextPart" or "TemplateID" must be provided.',
                                "ErrorRelatedTo": [
                                    "TextPart",
                                    "HTMLPart",
                                    "TemplateID",
                                ],
                            }
                        ],
                    }
                ]
            }

            email_scheduler_err = EmailScheduler.objects.create(
                email_to="abc@gmail.com",
                email_subject="Test subject 2 ",
                email_body="body",
            )

            EmailService.send_email(
                email_scheduler_obj_id=email_scheduler_err.pk,
                max_retries=3,
                retry_count=0,
            )

            no_email_log = EmailSchedulerLogs.objects.filter(
                email_scheduler=email_scheduler_err
            )
            self.assertFalse(no_email_log.exists())

            email_scheduler_err.refresh_from_db()
            self.assertEqual(email_scheduler_err.task_failed_count, 1)
            self.assertEqual(
                email_scheduler_err.task_failure_info,
                mock_mailjet_email_sender.return_value["Messages"][0]["Errors"],
            )
            self.assertEqual(email_scheduler_err.task_status, TASK_STATUS_FAILED)


    @patch(
        "apps.email_scheduler.email_sender.MailjetEmailWrapper.send_email_with_service"
    )
    def test_send_email_failed_with_retry(self, mock_mailjet_email_sender):
        mock_mailjet_email_sender.return_value = {
            "Messages": [
                {
                    "Status": "error",
                    "Errors": [
                        {
                            "ErrorIdentifier": "1",
                            "ErrorCode": "code-01",
                            "StatusCode": 429,
                            "ErrorMessage": "Error 429 occ",
                            "ErrorRelatedTo": ["TextPart", "HTMLPart", "TemplateID"],
                        }
                    ],
                }
            ]
        }

        email_scheduler_err = EmailScheduler.objects.create(
            email_to="abc@gmail.com", email_subject="Test subject 2 ", email_body="test"
        )
        with self.assertRaises(EmailSendingFailedWith429or500):
            EmailService.send_email(
                email_scheduler_obj_id=email_scheduler_err.pk,
                max_retries=3,
                retry_count=0,
            )
        email_scheduler_err.refresh_from_db()
        self.assertEqual(email_scheduler_err.task_status, TASK_STATUS_PENDING)
