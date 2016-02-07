import threading
import socket
from models import Contact, Constants
from models.Client import Client



class Server (threading.Thread):
    "A class for a Server instance."""
    def __init__(self, port, ui_manager, client_manager):
        threading.Thread.__init__(self)
        self.port = port
        self.ui_manager = ui_manager
        self.client_manager = client_manager


    def run(self):
        while(True): # This might need to be around the s.listen call
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', self.port))

        # if not self.connection_manager.has_connections():
        #     self.ui_manager.writeToScreen(
        #         "Socket is good, waiting for connections on port: " +
        #         str(self.port), "System")
            s.listen(1)

            self._handle_new_client(*s.accept())


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
        client = Client(conn)
        #conn_array.append(conn)  # add an array entry for this connection

        #self.ui_manager.writeToScreen("Connected by " + str(addr[0]), "System")

        global statusConnect
        statusConnect.set("Disconnect")
        #connecter.config(state=NORMAL) # UI piece

        client.establish_security_key_as_server()
        #self.connection_manager.establish_security_key(conn)

        client.send_message(username)

        client_username = client.receive_message()

        if client_username == "Self":
            client_username = addr[0]

        client.username = client_username

        self.client_manager.register_client(client)
        #self.connection_manager.register_contact(conn, Contact.Contact(client_username, str(addr[0]), str(self.port)))

        self.client_manager.send_peers(client)
