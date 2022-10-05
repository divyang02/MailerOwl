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
