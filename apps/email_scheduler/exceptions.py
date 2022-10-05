class EmailSendingFailedWith429or500(Exception):
    def __init__(self, message="Email sending failed with https status 429 or 500"):
        super().__init__(message)
