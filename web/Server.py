import socket
import threading

from web.Client import Client
from managers.ClientManager import ClientManager


class Server (threading.Thread):
    "A class for a Server instance."""
    def __init__(self, port, ui_manager):
        threading.Thread.__init__(self)
        self.port = port
        self.ui_manager = ui_manager
        self.client_manager = ClientManager(self.ui_manager)
        self.active = False

    def run(self):
        self.active = True
        while self.active: # This might need to be around the s.listen call
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', self.port))

            if self.client_manager.number_of_registered_clients() == 0:
                self.client_manager.write_system_message("Socket is good, waiting for connections port %d." % self.port)
            s.listen(1)

            self._handle_new_client(*s.accept())

        s.close()

    def _handle_new_client(self, conn_init, addr_init):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind(('', 0))  # get a random empty port
        serv.listen(1)

        portVal = str(serv.getsockname()[1]) # TODO why magic 5?
        if len(portVal) == 5:
            conn_init.send(portVal.encode())
        else:
            conn_init.send(("0" + portVal).encode())

        conn_init.close()
        conn, addr = serv.accept()
        client = Client(self.client_manager, conn)

        self.client_manager.write_system_message("Connected by %s." % addr[0])

        global statusConnect
        statusConnect.set("Disconnect")
        #connecter.config(state=NORMAL) # UI piece

        client.establish_security_key_as_server()

        client.send_message(self.client_manager.get_contact_manager().get_local_username())

        client_username = client.receive_message()

        if client_username == "Self":
            client_username = addr[0]

        client.username = client_username

        self.client_manager.register_client(client, client_username)

        self.client_manager.send_peers(client)

    def stop(self):
        self.active = False