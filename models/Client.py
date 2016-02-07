from Networked import Networked
from Constants import Command
import socket
import threading

class Client(Networked):
    def __init__(self, connection=None, client_username="Self"):
        super(Client, self).__init__(connection)
        self.client_username = client_username
        self.client_listener = None
        if connection:
            self.client_listener = ClientListener(self.connection)
            self.client_listener.start()


    def establish_security_key_as_server(self):
        (prime, base, a) = self.encryptor.generate_new_diffie_hellman_set()

        self._send(base)
        self._send(prime)
        self._send(pow(base, a) % prime)

        b = int(self._receive())
        secret_key = pow(b, a) % prime
        self.encryptor.set_key(secret_key)

    def establish_security_key_as_client(self):

        base = self._receive()
        prime = self._receive()
        a = self._receive()

        (_, _, b) = self.encryptor.generate_new_diffie_hellman_set()

        self._send(pow(base, b) % prime)

        secret_key = pow(a, b) % prime
        self.encryptor.set_key(secret_key)

    def connect_to_server(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(5.0)
        try:
            self.connection.connect((host, port))
        except socket.timeout:
            #writeToScreen("Timeout issue. Host possible not there.", "System")
            #connecter.config(state=NORMAL)
            raise SystemExit(0)
        except socket.error:
            #writeToScreen(
            #    "Connection issue. Host actively refused connection.", "System")
            #connecter.config(state=NORMAL)
            raise SystemExit(0)

        permanent_port = int(self._receive(5))
        self.connection.close() # disconnect from new connection port and move to permanent port

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, permanent_port))

        self.client_listener = ClientListener(self.connection)
        self.client_listener.start()


class ClientListener(Networked, threading.Thread):

    def __init__(self, connection):
        super(ClientListener, self).__init__(connection)
        self.connection = connection

    def run(self):
        while True:
            message = self.receive_message()
            if isinstance(message, Command):
                self.handle_command(message)
            else:
                pass # handle as a message


    def handle_command(self, command):
        pass
