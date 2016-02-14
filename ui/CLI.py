from ui.UI import UI


class CLI(UI):

    def __init__(self):
        super(CLI, self).__init__()

    def print_message(self, message):
        print message

