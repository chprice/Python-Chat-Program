class UiManager(object):

    def __init__(self):
        pass

    def writeToScreen(self, text, username=""):
        print(text)
        pass

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