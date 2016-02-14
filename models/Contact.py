class Contact(object):

    def __init__(self, username, host, port):
        self.username = username if username else host
        self.host = host
        self.port = port