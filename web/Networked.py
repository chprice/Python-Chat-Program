import logging
import socket

from models.Constants import Command
from util import util
from util.Encryptor import Encryptor


class Networked(object):

    def __init__(self, connection):
        self.connection = connection
        self.encryptor = Encryptor()

    def _send_encrypted(self, message):
        self._send(self.encryptor.encrypt(message))

    def _send(self, message, size=4):
        try:
            self.connection.send(util.format_number(len(str(message)), size).encode())
            self.connection.send(message.encode())
        except socket.error:
            logging.exception("Failed to send message.")

    def _receive(self, size=4):
        message_size = self.connection.recv(size).decode()
        if message_size[0] == '-':
            command_body = self._receive_encrypted()
            return Command(self.connection, message_size, command_body)

        message = self.connection.recv(int(message_size)).decode()
        return message

    def _receive_encrypted(self):
        encrypted_message = self._receive()
        if isinstance(encrypted_message, Command):
            return encrypted_message
        return self.encryptor.decrypt(encrypted_message)

    def send_message(self, message):
        self._send_encrypted(message)

    def receive_message(self):
        return self._receive_encrypted()

    def send_command(self, command):
        self._send(command)

    def _close(self):
        if self.connection:
            try:
                self.connection.close()
            except socket.error:
                print("Issue with someone being bad about disconnecting")
            except Exception as ex:
                print "Unknown error occurred", ex

