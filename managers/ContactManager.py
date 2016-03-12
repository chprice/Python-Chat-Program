class ContactManager(object):

    def __init__(self, local_username="Self"):
        self.contacts = {}
        self.local_username = local_username

    def add_contact(self, connection, contact):
        self.contacts[connection] = contact

    def update_contact_username(self, connection, username):
        self.contacts[connection].username = username

    def remove_contact(self, connection):
        self.contacts.pop(connection)

    def is_username_free(self, username):
        return not any([username == contact.username for contact in self.contacts])

    def change_local_username(self, username):
        self.local_username = username

    def get_username(self, connection):
        if connection in self.contacts:
            return self.contacts[connection].username
        return connection.getsockname()[0]

    def get_local_username(self):
        return self.local_username
