class ContactManager(object):

    def __init__(self):
        self.username_array = {}  # key: the open sockets in conn_array,
        # value: usernames for the connection
        self.contact_array = {}  # key: ip address as a string, value: [port, username]

        self.contacts = {}

    def add_contact(self, conn, contact):
        self.contacts[conn] = contact
        self.username_array[conn] = contact
        self.contact_array[contact.host] = contact

    def remove_contact(self, conn):
        self.contacts.pop(conn)

        #username_array[conn] = client_username
        #contact_array[str(addr[0])] = [str(self.port), client_username]


