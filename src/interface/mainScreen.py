import tkinter as tk
from interface.chat import Chat
from user import UserInfo

class MainScreen(tk.Frame):
    def __init__(self, master=None, user=None):
        tk.Frame.__init__(self, master)
        self._master = master
        
        self._user = user
        self._user.mainScreenAddUser = self.create_new_user
        self._user.chatAddUserMsg = self.addUserChatToHistory

        self._main_container = tk.Frame(self, bg="#fff")
        self._main_container.pack(expand=1, fill="both")

        self._users_button = dict()
        self._users_chats = dict()
        self._current_chat_id = None

        self._menu, self._users_list = self._create_menu(self._main_container)

    def _switch_chat(self, userId):
        """Destroys current frame and replaces it with a new one."""    
        if self._current_chat_id is not None:
            oldUserId = self._current_chat_id
            self._users_button[oldUserId].config(relief='raised')
            self._users_chats[oldUserId].pack_forget()

        self._current_chat_id = userId
        self._users_button[userId].config(relief='sunken')
        self._users_chats[userId].config(bg="#fff")
        self._users_chats[userId].pack(expand=1, fill="both")

    def addUserChatToHistory(self, userId, msg):
        if userId in self._users_chats.keys():
            self._users_chats[userId].add_user_msg(userId, msg)

    def disconnectUser(self):
        #enviar msg ao servidor com status desativo
        self._user.disconnect()
        del self._user
        self._user = None
        self._master.switch_frame('InitialScreen')

    def _create_menu(self, parent):
        menu_container = tk.Frame(parent)
        menu_container.config(background="#b3b3b3")
        menu_container.pack(side="left", fill="y")

        self._create_status_menu(menu_container)
        users_list_container = self._create_users_list_container(menu_container)

        return menu_container, users_list_container

    def _create_status_menu(self, parent):
        status_menu_container = tk.Frame(parent)
        status_menu_container.pack(side="top", fill="x")

        disconnect_container = tk.Frame(status_menu_container)
        disconnect_container.pack(padx=10, pady=10, anchor='center')

        disconnect = tk.Button(disconnect_container)
        disconnect["command"] = self.disconnectUser
        disconnect.config(text="Desconectar", font=("Arial", "10"), width=10)
        disconnect.pack()

        return status_menu_container

    def _create_users_list_container(self, parent):
        users_container = tk.Frame(parent)
        users_container.pack(padx=3, pady=5)

        for userId, userData in self._user.usersList.items():
            if userId == self._user.id:
                continue

            user_chat_history = Chat(self._main_container, self._user, userId, userData.name)
            user_chat_history.config(bg="#fff")
            self._users_chats[userId] = user_chat_history

            user_chat_button = tk.Button(users_container, command=lambda id=userId: self._switch_chat(id))
            user_chat_button.config(text=userData.name, font=("Arial", "10"), width=20, height=2)
            user_chat_button.pack()
            self._users_button[userId] = user_chat_button

            if self._current_chat_id is None:
                self._current_chat_id = userId
                user_chat_button.config(relief='sunken')
                user_chat_history.pack(expand=1, fill="both")

        return users_container

    def create_new_user(self, userInfo):
        user_chat_history = Chat(self._main_container, self._user, userInfo.id, userInfo.name)
        self._users_chats[userInfo.id] = user_chat_history

        user_chat_button = tk.Button(self._users_list, command=lambda id=userInfo.id: self._switch_chat(id))
        user_chat_button.config(text=userInfo.name, font=("Arial", "10"), width=20, height=2)
        user_chat_button.pack()

        self._users_button[userInfo.id] = user_chat_button
        return