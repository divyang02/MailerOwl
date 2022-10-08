class EmailSendingFailedWith429or500(Exception):
    """
    Exception raised when email sending failed with https status 429 or 500
    """

    def __init__(self,
                 message="Email sending failed with https status 429 or 500"):
        """
        Constructor for EmailSendingFailedWith429or500
        Arguments:
            message {str} -- Message to be displayed
        """
        super().__init__(message)
