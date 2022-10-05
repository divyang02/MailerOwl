from .constants import *
from .email_sender.abstract_email_sender import AbstractEmailSender
from django.utils import timezone
from django.db import transaction, DatabaseError
from django.db.models import F, Q
from .exceptions import EmailSendingFailedWith429or500
from http import HTTPStatus


class EmailService:
    @classmethod
    def _get_email_sender_class(cls, sender_name: str):
        """
        This method is used to get the correct class depending on the given name for the service
        """
        for sender_class in AbstractEmailSender.__subclasses__():
            if sender_class.email_service_used() == sender_name:
                return sender_class

    
    @classmethod
    def send_email(
        cls, email_scheduler_obj_id: int, max_retries: int, retry_count: int
    ):
        from .models import EmailScheduler, EmailSchedulerLogs

        email_scheduler_obj = EmailScheduler.objects.get(pk=email_scheduler_obj_id)

        email_sender = cls._get_email_sender_class(email_scheduler_obj.email_service)
        response = email_sender.send_email_with_service(email_scheduler_obj)
        (
            status,
            parsed_response,
        ) = email_sender.parse_response_for_email_scheduler_logs_creation_and_email_scheduler_updation(
            response, retry_count, email_scheduler_obj
        )

        is_email_send_successfully = status == EMAIL_SEND_STATUS_SUCCESS

        if is_email_send_successfully:
            cls._create_email_scheduler_logs(parsed_response)
        cls._update_email_scheduler(
            email_scheduler_obj=email_scheduler_obj,
            parsed_response=parsed_response,
            max_retries=max_retries,
            retry_count=retry_count,
            success=is_email_send_successfully,
        )
