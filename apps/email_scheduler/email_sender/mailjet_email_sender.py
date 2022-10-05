from .abstract_email_sender import AbstractEmailSender
from django.conf import settings
from mailjet_rest import Client
from ..constants import *


class MailjetEmailWrapper(AbstractEmailSender):
    mailjet_send = Client(
        auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version="v3.1"
    )
    mailjet_retrieve = Client(
        auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET)
    )

    @classmethod
    def parse_response_for_email_scheduler_logs_creation_and_email_scheduler_updation(
        cls, response: dict, retry_count: int, email_scheduler_object
    ):
        if response["Messages"][0]["Status"] == EMAIL_SEND_STATUS_SUCCESS:
            logs_to_be_created = []

            keys_to_extract = ["To", "Cc", "Bcc"]

            response_messages = {
                key: response["Messages"][0][key] for key in keys_to_extract
            }

            for email_recipient_type, emails in response_messages.items():
                for email in emails:
                    logs_to_be_created.append(
                        {
                            "email_scheduler": email_scheduler_object,
                            "email_recipient_id": email["Email"],
                            "retry_count": retry_count,
                            "email_message_id": email["MessageID"],
                            "email_recipient_type": email_recipient_type.lower(),
                        }
                    )

            return EMAIL_SEND_STATUS_SUCCESS, logs_to_be_created
        else:
            return EMAIL_SEND_STATUS_ERROR, response["Messages"][0]["Errors"]

    @classmethod
    def email_service_used(cls):
        return EMAIL_SERVICE_MAILJET

    @classmethod
    def send_email_with_service(cls, email_scheduler_object):
        email_cc = [{"Email": cc} for cc in email_scheduler_object.email_cc]
        email_bcc = [{"Email": bcc} for bcc in email_scheduler_object.email_bcc]

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": DEFAULT_FROM_EMAIL,
                    },
                    "To": [
                        {
                            "Email": email_scheduler_object.email_to,
                        }
                    ],
                    "Cc": email_cc,
                    "Bcc": email_bcc,
                    "Subject": email_scheduler_object.email_subject,
                    "HTMLPart": email_scheduler_object.email_body,  # This is in HTMLPart because in TextPart if we put body then status does not get updated
                }
            ]
        }

        result = cls.mailjet_send.send.create(data=data)
        return result.json()

    @classmethod
    def fetch_email_status_by_message_id(cls, message_id: str):
        result = cls.mailjet_retrieve.messagehistory.get(id=message_id).json()
        if len(result["Data"]) == 0:
            return None
        recent_event = result["Data"][-1]
        return recent_event
