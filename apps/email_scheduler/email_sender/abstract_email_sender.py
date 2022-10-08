class AbstractEmailSender(object):

    @classmethod
    def parse_response_for_email_scheduler_logs_creation_and_email_scheduler_updation(
            cls, response: dict, retry_count: int, email_scheduler_object):
        """
        This method will parse the response and return a tuple, with first element as "Success"/"Error"
        and second element will be a list of dict. In case of success, second element will contain list of
        dict for creating logs and in case of error the second element will contain list of dict of errors with
        each dict containing a key "StatusCode"
        Arguments:
            response {dict} -- Response from the email service
            retry_count {int} -- Retry count of the email scheduler
            email_scheduler_object {object} -- Email scheduler object
        Returns:
            Error -- NotImplementedError
        """
        raise NotImplementedError

    @classmethod
    def email_service_used(cls):
        """
        This method should be overrided to return a string of which email sending service is being used
        Arguments:
            None
        Returns:
            Error -- NotImplementedError
        """
        raise NotImplementedError

    @classmethod
    def send_email_with_service(cls, email_scheduler_object):
        """
        This method is overrided to send an email using the specific service. It takes object of
        EmailScheduler as an argument. It should return JSON containing response given by service
        Arguments:
            email_scheduler_object {object} -- Email scheduler object
        Returns:
            Error -- NotImplementedError
        """
        raise NotImplementedError

    @classmethod
    def fetch_email_status_by_message_id(cls, message_id: str):
        """
        This method should be overrided to check the status of a message using message id. It should
        return a dict which is returned by the service. We need to make sure that dict has a key named
        EventType which clearly specifies the event like "sent", "opened", "hardbounce" etc.
        Arguments:
            message_id {str} -- Message id of the email
        Returns:
            Error -- NotImplementedError
        """
        raise NotImplementedError
