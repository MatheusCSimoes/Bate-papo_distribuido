import tkinter as tk
from interface.chat import Chat

class MainScreen(tk.Frame):
    def __init__(self, master=None, user=None):
        tk.Frame.__init__(self, master)
        self._master = master
        
        self._user = user

        self._main_container = tk.Frame(self, bg="#fff")
        self._main_container.pack(expand=1, fill="both")

        self._menu = self.__create_menu(self._main_container)
        
        self._current_chat = Chat(self._main_container, self._user, 1, chatHistory=[(1, 'testando'), (1, 'hehe')])
        self._current_chat.config(bg="#fff")
        self._current_chat.pack(expand=1, fill="both")
        
        self._chat_frame = None
        #self.switch_frame(LogIn)

    def __switch_chat(self, userId):
        """Destroys current frame and replaces it with a new one."""
        '''
        new_frame = frame_class(self)
        if self._chat_frame is not None:
            self._chat_frame.destroy()
        self._chat_frame = new_frame
        self._chat_frame.config(bg="#fff")
        self._chat_frame.pack(expand=1, fill="both")'''

    def __disconnectUser(self):
        #enviar msg ao servidor com status desativo

        self._master.switch_frame('InitialScreen')

    def __create_menu(self, parent):
        menu_container = tk.Frame(parent)
        menu_container.config(background="#b3b3b3")
        menu_container.pack(side="left", fill="y")

        self.__create_status_menu(menu_container)
        self.__create_users_list_container(menu_container, [])

        return menu_container

    def __create_status_menu(self, parent):
        status_menu_container = tk.Frame(parent)
        status_menu_container.pack(side="top")

        disconnect_container = tk.Frame(status_menu_container)
        disconnect_container.pack(padx=10, pady=10, side="left")

        disconnect = tk.Button(disconnect_container)
        disconnect["command"] = self.__disconnectUser
        disconnect.config(text="Desconectar", font=("Arial", "10"), width=10)
        disconnect.pack()

        return status_menu_container

    def __create_users_list_container(self, parent, usersList):
        users_container = tk.Frame(parent)
        users_container.pack(side="bottom")

        return users_container

    def __create_new_user(self, parent, username, status):
        user_container = tk.Frame(parent)
        user_container.pack()

        user_name = tk.Label(user_container, text=username)
        user_name["font"] = ("Arial", "10")
        user_name.pack()

        return user_container    