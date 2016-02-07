import Constants
class ClientManager(object):

    def __init__(self):
        self.clients = []

    def register_client(self, client):
        self.clients.append(client)

    def unregister_client(self, client):
        self.clients.pop(client)

    def send_to_all(self, message):
        for client in self.clients:
            client.send_message(message)


    def send_peers(self, current_client_connection):
        current_client = self._client_from_connection(current_client_connection)
        for client in self.clients:
            if client != current_client:
                current_client.send_command(Constants.CONTACT_SEND)
                current_client.send_message(client.connection.getpeername()[0]) # send ip address


    def _client_from_connection(self, connection):
        for client in self.clients:
            if client.connection == connection:
                return client
        return None