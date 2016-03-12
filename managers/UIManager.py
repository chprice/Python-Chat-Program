class UIManager(object):

    def __init__(self, ui_type, network_manager=None):
        self.ui = ui_type(self)
        self.network_manager = network_manager


    def write_message(self, message):
        self.ui.write_message(message)

    def set_connection_status(self, status):
        self.ui.set_connection_status(status)

