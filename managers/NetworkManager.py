from web.Server import Server

class NetworkManager(object):

    def __init__(self, ui_manager=None):
        self.server = None
        self.ui_manager = ui_manager

    def start_server(self, port):
        if not self.server:
            self.server = Server(port, self.ui_manager)

    def disconnect(self):
        if self.server:
            self.server.stop()