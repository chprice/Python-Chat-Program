import sys
import socket

from managers import NetworkManager, UIManager
from ui import GUI, CLI



def __main__():
    version = 2
    if sys.hexversion <= 0x03000000:
        version = 3

    ui_type = GUI.GUI
    if len(sys.argv) > 1 and sys.argv[1] == "-cli":
        print("Starting command line chat")
        ui_type = CLI.CLI

    ui_manger = UIManager.UIManager(ui_type)
    network_manger = NetworkManager.NetworkManager(ui_manger)
    ui_manger.network_manager = network_manger







# GLOBALS




username = "Self"

location = 0
port = 0
top = ""

main_body_text = 0






def processUserCommands(command, param):
    """Processes commands passed in via the / text input."""
    global conn_array
    global secret_array
    global username

    if command == "nick":  # change nickname
        for letter in param[0]:
            if letter == " " or letter == "\n":
                if isCLI:
                    error_window(0, "Invalid username. No spaces allowed.")
                else:
                    error_window(root, "Invalid username. No spaces allowed.")
                return
        if isUsernameFree(param[0]):
            writeToScreen("Username is being changed to " + param[0], "System")
            for conn in conn_array:
                conn.send("-002".encode())
                netThrow(conn, secret_array[conn], param[0])
            username = param[0]
        else:
            writeToScreen(param[0] +
                          " is already taken as a username", "System")
    if command == "disconnect":  # disconnects from current connection
        for conn in conn_array:
            conn.send("-001".encode())
        processFlag("-001")
    if command == "connect":  # connects to passed in host port
        if(options_sanitation(param[1], param[0])):
            Client(param[0], int(param[1])).start()
    if command == "host":  # starts server on passed in port
        if(options_sanitation(param[0])):
            Server(int(param[0])).start()

def isUsernameFree(name):
    """Checks to see if the username name is free for use."""
    global username_array
    global username
    for conn in username_array:
        if name == username_array[conn] or name == username:
            return False
    return True








    dump_contacts()
