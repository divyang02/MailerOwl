class AbstractEmailSender(object):
    
    @classmethod
    def email_service_used(cls):
        """
        This method should be overrided to return a string of which email sending service is being used
        """
        raise NotImplementedError

    @classmethod
    def send_email_with_service(cls, email_scheduler_object):
        """
        This method is overrided to send an email using the specific service. It takes object of
        EmailScheduler as an argument. It should return JSON containing response given by service
        """
        raise NotImplementedError
