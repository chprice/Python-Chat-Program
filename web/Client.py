import socket
import threading

from models.Constants import *
from web.Networked import Networked


class Client(Networked):
    def __init__(self, client_manager, connection=None):
        super(Client, self).__init__(connection)
        self.client_manager = client_manager
        self.client_listener = None
        if connection:
            self.client_listener = ClientListener(self.client_manager, self.connection)
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
            self.client_manager.write_system_message("Timeout issue. Host possible not there.")
            self.client_manager
            #connecter.config(state=NORMAL)
            raise SystemExit(0)
        except socket.error:
            self.client_manager.write_system_message("Connection issue. Host actively refused connection.")
            #connecter.config(state=NORMAL)
            raise SystemExit(0)

        permanent_port = int(self._receive(5))
        self.connection.close() # disconnect from new connection port and move to permanent port

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, permanent_port))

        self.client_listener = ClientListener(self.client_manager, self.connection)
        self.client_listener.start()

    def close(self):
        if self.client_listener:
            self.client_listener._close()
        self._close()


class ClientListener(Networked, threading.Thread):

    def __init__(self, client_manager, connection):
        super(ClientListener, self).__init__(connection)
        self.client_manager = client_manager
        self.connection = connection

    def run(self):
        while True:
            message = self.receive_message()
            if isinstance(message, Command):
                self.handle_command(message)
            else:
                self.client_manager.write_message(self.connection, message)

    def handle_command(self, command):
        try:
            if command.operation == DISCONNECT:
                self.client_manager.close_connection(command.connection)
                self.client_manager.write_system_message(
                    "Connect to " + command.connection.getsockname()[0] + " closed.")

            elif command.operation == USERNAME_CHANGE:
                username = command.message
                if self.client_manager.get_contact_manager().is_username_free(username):
                    self.client_manager.write_system_message("User %s has changed their username to %s." %
                            (self.client_manager.get_contact_manager().get_username(command.connection), username))
                    self.client_manager.get_contact_manager().update_contact_username(command.connection)

            elif command.operation == CONTACT_SEND:
                ip_address, port = command.message.split(":")
                Client(self.client_manager).connect_to_server(ip_address, port)

        except Exception as ex:
            print "Error while processing command:", ex
