from Tkinter import *
from tkFileDialog import asksaveasfilename

#--------------------------------------------------------------------------



def client_options_go(dest, port, window):
    "Processes the options entered by the user in the client options window."""
    if options_sanitation(port, dest):
        if not isCLI:
            window.destroy()
        Client(dest, int(port)).start()
    elif isCLI:
        sys.exit(1)

def options_sanitation(por, loc=""):
    """Checks to make sure the port and destination ip are both valid.
    Launches error windows if there are any issues.

    """
    global root
    if version == 2:
        por = unicode(por)
    if isCLI:
        root = 0
    if not por.isdigit():
        error_window(root, "Please input a port number.")
        return False
    if int(por) < 0 or 65555 < int(por):
        error_window(root, "Please input a port number between 0 and 65555")
        return False
    if loc != "":
        if not ip_process(loc.split(".")):
            error_window(root, "Please input a valid ip address.")
            return False
    return True

def ip_process(ipArray):
    """Checks to make sure every section of the ip is a valid number."""
    if len(ipArray) != 4:
        return False
    for ip in ipArray:
        if version == 2:
            ip = unicode(ip)
        if not ip.isdigit():
            return False
        t = int(ip)
        if t < 0 or 255 < t:
            return False
    return True

#------------------------------------------------------------------------------

def server_options_window(master):
    """Launches server options window for getting port."""
    top = Toplevel(master)
    top.title("Connection options")
    top.grab_set()
    top.protocol("WM_DELETE_WINDOW", lambda: optionDelete(top))
    Label(top, text="Port:").grid(row=0)
    port = Entry(top)
    port.grid(row=0, column=1)
    port.focus_set()
    go = Button(top, text="Launch", command=lambda:
    server_options_go(port.get(), top))
    go.grid(row=1, column=1)

def server_options_go(port, window):
    """Processes the options entered by the user in the
    server options window.

    """
    if options_sanitation(port):
        if not isCLI:
            window.destroy()
        Server(int(port)).start()
    elif isCLI:
        sys.exit(1)

#-------------------------------------------------------------------------

def username_options_window(master):
    """Launches username options window for setting username."""
    top = Toplevel(master)
    top.title("Username options")
    top.grab_set()
    Label(top, text="Username:").grid(row=0)
    name = Entry(top)
    name.focus_set()
    name.grid(row=0, column=1)
    go = Button(top, text="Change", command=lambda:
    username_options_go(name.get(), top))
    go.grid(row=1, column=1)


def username_options_go(name, window):
    """Processes the options entered by the user in the
    server options window.

    """
    processUserCommands("nick", [name])
    window.destroy()

#-------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# Contacts window

def contacts_window(master):
    """Displays the contacts window, allowing the user to select a recent
    connection to reuse.

    """
    global contact_array
    cWindow = Toplevel(master)
    cWindow.title("Contacts")
    cWindow.grab_set()
    scrollbar = Scrollbar(cWindow, orient=VERTICAL)
    listbox = Listbox(cWindow, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    buttons = Frame(cWindow)
    cBut = Button(buttons, text="Connect",
                  command=lambda: contacts_connect(
                      listbox.get(ACTIVE).split(" ")))
    cBut.pack(side=LEFT)
    dBut = Button(buttons, text="Remove",
                  command=lambda: contacts_remove(
                      listbox.get(ACTIVE).split(" "), listbox))
    dBut.pack(side=LEFT)
    aBut = Button(buttons, text="Add",
                  command=lambda: contacts_add(listbox, cWindow))
    aBut.pack(side=LEFT)
    buttons.pack(side=BOTTOM)

    for person in contact_array:
        listbox.insert(END, contact_array[person][1] + " " +
                       person + " " + contact_array[person][0])
    listbox.pack(side=LEFT, fill=BOTH, expand=1)

def contacts_connect(item):
    """Establish a connection between two contacts."""
    Client(item[1], int(item[2])).start()

def contacts_remove(item, listbox):
    """Remove a contact."""
    if listbox.size() != 0:
        listbox.delete(ACTIVE)
        global contact_array
        h = contact_array.pop(item[1])


def contacts_add(listbox, master):
    """Add a contact."""
    aWindow = Toplevel(master)
    aWindow.title("Contact add")
    Label(aWindow, text="Username:").grid(row=0)
    name = Entry(aWindow)
    name.focus_set()
    name.grid(row=0, column=1)
    Label(aWindow, text="IP:").grid(row=1)
    ip = Entry(aWindow)
    ip.grid(row=1, column=1)
    Label(aWindow, text="Port:").grid(row=2)
    port = Entry(aWindow)
    port.grid(row=2, column=1)
    go = Button(aWindow, text="Add", command=lambda:
    contacts_add_helper(name.get(), ip.get(), port.get(),
                        aWindow, listbox))
    go.grid(row=3, column=1)


def contacts_add_helper(username, ip, port, window, listbox):
    """Contact adding helper function. Recognizes invalid usernames and
    adds contact to listbox and contact_array.

    """
    for letter in username:
        if letter == " " or letter == "\n":
            error_window(root, "Invalid username. No spaces allowed.")
            return
    if options_sanitation(port, ip):
        listbox.insert(END, username + " " + ip + " " + port)
        contact_array[ip] = [port, username]
        window.destroy()
        return

def load_contacts():
    """Loads the recent chats out of the persistent file contacts.dat."""
    global contact_array
    try:
        filehandle = open("data\\contacts.dat", "r")
    except IOError:
        return
    line = filehandle.readline()
    while len(line) != 0:
        temp = (line.rstrip('\n')).split(" ")  # format: ip, port, name
        contact_array[temp[0]] = temp[1:]
        line = filehandle.readline()
    filehandle.close()

def dump_contacts():
    """Saves the recent chats to the persistent file contacts.dat."""
    global contact_array
    try:
        filehandle = open("data\\contacts.dat", "w")
    except IOError:
        print("Can't dump contacts.")
        return
    for contact in contact_array:
        filehandle.write(
            contact + " " + str(contact_array[contact][0]) + " " +
            contact_array[contact][1] + "\n")
    filehandle.close()

#-----------------------------------------------------------------------------

# places the text from the text bar on to the screen and sends it to
# everyone this program is connected to
def placeText(text):
    """Places the text from the text bar on to the screen and sends it to
    everyone this program is connected to.

    """
    global conn_array
    global secret_array
    global username
    writeToScreen(text, username)
    for person in conn_array:
        netThrow(person, secret_array[person], text)



def processUserText(event):
    """Takes text from text bar input and calls processUserCommands if it
    begins with '/'.

    """
    data = text_input.get()
    if data[0] != "/":  # is not a command
        placeText(data)
    else:
        if data.find(" ") == -1:
            command = data[1:]
        else:
            command = data[1:data.find(" ")]
        params = data[data.find(" ") + 1:].split(" ")
        processUserCommands(command, params)
    text_input.delete(0, END)


def processUserInput(text):
    """ClI version of processUserText."""
    if text[0] != "/":
        placeText(text)
    else:
        if text.find(" ") == -1:
            command = text[1:]
        else:
            command = text[1:text.find(" ")]
        params = text[text.find(" ") + 1:].split(" ")
        processUserCommands(command, params)


        #-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Menu helpers

def QuickClient():
    """Menu window for connection options."""
    window = Toplevel(root)
    window.title("Connection options")
    window.grab_set()
    Label(window, text="Server IP:").grid(row=0)
    destination = Entry(window)
    destination.grid(row=0, column=1)
    go = Button(window, text="Connect", command=lambda:
    client_options_go(destination.get(), "9999", window))
    go.grid(row=1, column=1)


def QuickServer():
    """Quickstarts a server."""
    Server(9999).start()

def saveHistory():
    """Saves history with Tkinter's asksaveasfilename dialog."""
    global main_body_text
    file_name = asksaveasfilename(
        title="Choose save location",
        filetypes=[('Plain text', '*.txt'), ('Any File', '*.*')])
    try:
        filehandle = open(file_name + ".txt", "w")
    except IOError:
        print("Can't save history.")
        return
    contents = main_body_text.get(1.0, END)
    for line in contents:
        filehandle.write(line)
    filehandle.close()


def connects(clientType):
    global conn_array
    connecter.config(state=DISABLED)
    if len(conn_array) == 0:
        if clientType == 0:
            client_options_window(root)
        if clientType == 1:
            server_options_window(root)
    else:
        # connecter.config(state=NORMAL)
        for connection in conn_array:
            connection.send("-001".encode())
        processFlag("-001")


def toOne():
    global clientType
    clientType = 0


def toTwo():
    global clientType
    clientType = 1


#-------------------------------------------------------------------------


if len(sys.argv) > 1 and sys.argv[1] == "-cli":
    print("Starting command line chat")

else:
