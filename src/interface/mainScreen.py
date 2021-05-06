import tkinter as tk
from interface.chat import Chat

class MainScreen(tk.Frame):
    def __init__(self, master=None, user=None):
        tk.Frame.__init__(self, master)
        self._master = master
        
        self._user = user

        self._main_container = tk.Frame(self, bg="#fff")
        self._main_container.pack(expand=1, fill="both")

        self._users_button = dict()
        self._users_chats = dict()
        self._current_chat = None

        self._menu = self.__create_menu(self._main_container)

    def __switch_chat(self, userId):
        """Destroys current frame and replaces it with a new one."""        
        if self._current_chat is not None:
            self._current_chat.pack_forget()

        self._current_chat = self._users_chats[userId]
        self._current_chat.config(bg="#fff")
        self._current_chat.pack(expand=1, fill="both")

        self._user.chatAddUserMsg = self._current_chat.add_user_msg

    def __disconnectUser(self):
        #enviar msg ao servidor com status desativo
        self._user.disconnect()
        self._master.switch_frame('InitialScreen')

    def __create_menu(self, parent):
        menu_container = tk.Frame(parent)
        menu_container.config(background="#b3b3b3")
        menu_container.pack(side="left", fill="y")

        self.__create_status_menu(menu_container)
        self.__create_users_list_container(menu_container)

        return menu_container

    def __create_status_menu(self, parent):
        status_menu_container = tk.Frame(parent)
        status_menu_container.pack(side="top", fill="x")

        disconnect_container = tk.Frame(status_menu_container)
        disconnect_container.pack(padx=10, pady=10, anchor='center')

        disconnect = tk.Button(disconnect_container)
        disconnect["command"] = self.__disconnectUser
        disconnect.config(text="Desconectar", font=("Arial", "10"), width=10)
        disconnect.pack()

        return status_menu_container

    def __create_users_list_container(self, parent):
        users_container = tk.Frame(parent)
        users_container.pack(padx=3, pady=5)

        for userId, userData in self._user.usersList.items():
            user_chat_history = Chat(self._main_container, self._user, userId, userData.name, chatHistory=[('1', 'testando'), ('2', 'hehe')])

            if self._current_chat is None:
                self._current_chat = user_chat_history
                self._current_chat.config(bg="#fff")
                self._current_chat.pack(expand=1, fill="both")

            self._users_chats[userId] = user_chat_history

            user_chat_button = tk.Button(users_container, command=lambda id=userId: self.__switch_chat(id))
            user_chat_button.config(text=userData.name, font=("Arial", "10"), width=20, height=2)
            user_chat_button.pack()

            self._users_button[userId] = user_chat_button

        return users_container

    def create_new_user(self, parent, username, status):
        user_container = tk.Frame(parent)
        user_container.pack()

        user_name = tk.Label(user_container, text=username)
        user_name["font"] = ("Arial", "10")
        user_name.pack()

        return user_container    