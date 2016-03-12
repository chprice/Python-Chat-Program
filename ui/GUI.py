from Tkinter import *
from tkFileDialog import asksaveasfilename
from ui.UI import UI

class GUI(UI):

    def __init__(self, version=2):
        super(GUI, self).__init__()
        if version == 2:
            from Tkinter import *
            from tkFileDialog import asksaveasfilename
        if version == 3:
            from tkinter import *
            from tkinter.filedialog import asksaveasfilename

        self.main_window = Tk()


    def _build_main_window(self):
        main_window = Tk()
        main_window.title("Chat")

        menubar = Menu(main_window)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save chat", command=self._start_save_chat_window)
        file_menu.add_command(label="Change username",
                              command=self._start_username_options_window)
        file_menu.add_command(label="Exit", command=self.main_window.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        connection_menu = Menu(menubar, tearoff=0)
        connection_menu.add_command(label="Connect", command=self._start_client_options_window)

        connection_menu.add_command(
            label="Disconnect", command=lambda: processFlag("-001"))
        menubar.add_cascade(label="Connect", menu=connection_menu)

        server_menu = Menu(menubar, tearoff=0)
        server_menu.add_command(label="Launch server", command=QuickServer)
        server_menu.add_command(label="Listen on port",
                                command=lambda: server_options_window(root))
        menubar.add_cascade(label="Server", menu=server_menu)

        menubar.add_command(label="Contacts", command=lambda:
        contacts_window(root))

        root.config(menu=menubar)

        main_body = Frame(root, height=20, width=50)

        main_body_text = Text(main_body)
        body_text_scroll = Scrollbar(main_body)
        main_body_text.focus_set()
        body_text_scroll.pack(side=RIGHT, fill=Y)
        main_body_text.pack(side=LEFT, fill=Y)
        body_text_scroll.config(command=main_body_text.yview)
        main_body_text.config(yscrollcommand=body_text_scroll.set)
        main_body.pack()

        main_body_text.insert(END, "Welcome to the chat program!")
        main_body_text.config(state=DISABLED)

        text_input = Entry(root, width=60)
        text_input.bind("<Return>", processUserText)
        text_input.pack()

        statusConnect = StringVar()
        statusConnect.set("Connect")
        clientType = 1
        Radiobutton(root, text="Client", variable=clientType,
                    value=0, command=toOne).pack(anchor=E)
        Radiobutton(root, text="Server", variable=clientType,
                    value=1, command=toTwo).pack(anchor=E)
        connecter = Button(root, textvariable=statusConnect,
                           command=lambda: connects(clientType))
        connecter.pack()

        load_contacts()

        #------------------------------------------------------------#

        root.mainloop()

    def writeToScreen(self, text):
        pass


    def disconnect(self):
        self.ui_manager.network_manager
    #
    # if isCLI:
    #     if username:
    #         print(username + ": " + text)
    #     else:
    #         print(text)
    # else:
    #     main_body_text.config(state=NORMAL)
    #     main_body_text.insert(END, '\n')
    #     if username:
    #         main_body_text.insert(END, username + ": ")
    #     main_body_text.insert(END, text)
    #     main_body_text.yview(END)
    #     main_body_text.config(state=DISABLED)


    def _start_client_options_window(self, port=9999):
        """Launches client options window for getting destination hostname
        and port.

        """
        client_option_window = Toplevel(self.main_window)
        client_option_window.title("Connection options")
        client_option_window.protocol("WM_DELETE_WINDOW", lambda: optionDelete(top))
        client_option_window.grab_set()
        Label(client_option_window, text="Server IP:").grid(row=0)
        location = Entry(client_option_window)
        location.grid(row=0, column=1)
        location.focus_set()
        Label(client_option_window, text="Port:").grid(row=1)
        port = Entry(client_option_window)
        port.grid(row=1, column=1)
        go = Button(client_option_window, text="Connect", command=lambda:
        client_options_go(location.get(), port.get(), client_option_window))
        go.grid(row=2, column=1)

    def build_error_window(self, error_message):
        """Launches a new window to display the error message."""
            error_window = Toplevel(self.main_window)
            error_window.title("ERROR")
            error_window.grab_set()
            Label(error_window, text=error_message).pack()
            ok = Button(error_window, text="OK", command=error_window.destroy)
            ok.pack()
            ok.focus_set()

    def optionDelete(window):
        connecter.config(state=NORMAL)
        window.destroy()

    def _start_save_chat_window(self):
        pass

    def _start_username_options_window(self):
        pass