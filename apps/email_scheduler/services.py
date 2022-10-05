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
    def _create_email_scheduler_logs(cls, parsed_response: list):
        """This method is used to create email scheduler logs """
        from .models import EmailSchedulerLogs

        logs_to_be_created = parsed_response

        EmailSchedulerLogs.create_logs(logs_to_be_created)

    @classmethod
    def _update_email_scheduler(
        cls,
        email_scheduler_obj,
        parsed_response: list,
        max_retries: int,
        retry_count: int,
        success: bool,
    ):
        """This method is used to update email scheduler object after we send email"""
        if success:
            updated_fields = {
                "email_last_sent_at": timezone.now(),
                "email_send_count": email_scheduler_obj.email_send_count + 1,
            }
            if email_scheduler_obj.email_repeat_after is None:
                updated_fields["task_status"] = TASK_STATUS_COMPLETE
            email_scheduler_obj.update_fields(updated_fields)
        else:
            updated_fields = {
                "task_failed_count": email_scheduler_obj.task_failed_count + 1
            }

            errors = parsed_response

            error_429_or_500 = False
            for err in errors:
                if (
                    err["StatusCode"] == HTTPStatus.TOO_MANY_REQUESTS
                    or err["StatusCode"] == HTTPStatus.INTERNAL_SERVER_ERROR
                ):
                    error_429_or_500 = True
                    break
            updated_fields["task_failure_info"] = errors

            if retry_count < max_retries and error_429_or_500:
                email_scheduler_obj.update_fields(updated_fields)
                raise EmailSendingFailedWith429or500
            else:
                updated_fields["task_status"] = TASK_STATUS_FAILED
                email_scheduler_obj.update_fields(updated_fields)

    @classmethod
    def email_scheduler_log_updater(cls):
        """This method is used to update the logs"""
        from .models import EmailSchedulerLogs

        queryset = EmailSchedulerLogs.get_logs_to_be_updated()

        try:
            with transaction.atomic():
                for email_scheduler_logs in queryset:
                    email_sender = cls._get_email_sender_class(
                        email_scheduler_logs.email_scheduler.email_service
                    )
                    email_status = email_sender.fetch_email_status_by_message_id(
                        message_id=email_scheduler_logs.email_message_id
                    )
                    if email_status is not None:
                        email_scheduler_logs.update_fields(
                            {
                                "email_send_status": email_status["EventType"],
                                "email_event_info": email_status,
                            }
                        )
        except DatabaseError:
            pass

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
