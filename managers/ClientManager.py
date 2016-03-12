import models.Constants
from managers.ContactManager import ContactManager
from models.Contact import Contact


class ClientManager(object):

    def __init__(self, ui_manager):
        self.clients = []
        self.ui_manager = ui_manager
        self.contact_manager = ContactManager()

    def register_client(self, client, username=None):
        self.clients.append(client)
        self.contact_manager.add_contact(client.connection, Contact(username, *client.connection.getpeername()))

    def unregister_client(self, client):
        self.clients.pop(client)

    def send_to_all(self, message):
        for client in self.clients:
            client.send_message(message)

    def number_of_registered_clients(self):
        return len(self.clients)

    def send_peers(self, current_client_connection):
        current_client = self.client_from_connection(current_client_connection)
        for client in self.clients:
            if client != current_client:
                current_client.send_command(models.Constants.CONTACT_SEND)
                current_client.send_message(":".join([str(x) for x in client.connection.getpeername()])) # send ip address

    def client_from_connection(self, connection):
        for client in self.clients:
            if client.connection == connection:
                return client
        return None

    def close_connection(self, connection):
        client = self.client_from_connection(connection)
        client.close()
        self.unregister_client(client)

    def write_message(self, connection, message):
        self.ui_manager.write_message(self.contact_manager.get_username(connection) + ": " + message)

    def write_system_message(self, message):
        self.ui_manager.write_message("System: " + message)

    def get_contact_manager(self):
        return self.contact_manager

    def set_connection_status(self, state):
        self.ui_manager.set_connection_status(state)