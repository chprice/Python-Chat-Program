DISCONNECT = "-001"
USERNAME_CHANGE = "-002"
CONTACT_SEND = "-004"


class Command(object):
    def __init__(self, connection, operation, message):
        self.connection = connection
        self.operation = operation
        self.message = message

