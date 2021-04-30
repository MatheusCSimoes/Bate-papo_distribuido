import tkinter as tk

class Chat(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.chat_container = tk.Frame(self, bg="#fff")
        self.chat_container.pack(expand=1, fill="both")

        self.menu = _create_menu(self.chat_container) #inicia com status desconectado
        self.user_chat = _create_user_chat_container(self.chat_container)

def _create_menu(parent):
    menu_container = tk.Frame(parent)
    menu_container.config(background="#b3b3b3")
    menu_container.pack(side="left", fill="y")

    _create_status_menu(menu_container, 0)
    _create_users_list_container(menu_container, [])

    return menu_container

def _create_status_menu(parent, currentStatus):
    status_menu_container = tk.Frame(parent)
    status_menu_container.pack(side="top")

    connect_container = tk.Frame(status_menu_container)
    connect_container.pack(padx=10, pady=10, side="left")

    connect = tk.Button(connect_container)
    #connect["command"] = #enviar msg ao servidor com status ativo
    connect.config(text="Conectar", font=("Arial", "10"), width=10)
    connect.pack()

    disconnect_container = tk.Frame(status_menu_container)
    disconnect_container.pack(padx=10, pady=10, side="left")

    disconnect = tk.Button(disconnect_container)
    #disconnect["command"] = #enviar msg ao servidor com status desativo
    disconnect.config(text="Desconectar", font=("Arial", "10"), width=10)
    disconnect.pack()

    return status_menu_container

def _create_users_list_container(parent, usersList):
    users_container = tk.Frame(parent)
    users_container.pack(side="bottom")

    return users_container

def _create_user_chat_container(parent):
    message_container = tk.Frame(parent)
    message_container.pack(side="bottom", fill="x", pady=10, padx=10)

    message_entry = tk.Entry(message_container)
    message_entry.config(font=("Arial", "8"))
    
    send_button = tk.Button(message_container, command=lambda: send_message(message_entry))
    send_button.config(text="Enviar", font=("Arial", "7"), width=5, height=2)
    send_button.pack(side="right")

    message_entry.pack(side="right", padx=10, fill="x")

    return message_container

def send_message(msg_entry):
    print(msg_entry.get())

def create_new_user(parent, username, status):
    user_container = tk.Frame(parent)
    user_container.pack()

    user_name = tk.Label(user_container, text=username)
    user_name["font"] = ("Arial", "10")
    user_name.pack()

    return user_container    