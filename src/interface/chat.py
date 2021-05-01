import tkinter as tk

class Chat(tk.Frame):
    def __init__(self, master, user, userId, active=True, chatHistory=[]):
        tk.Frame.__init__(self, master)
        self._userActive = active
        self._userId = userId
        self._chat_history = chatHistory
        
        self._user = user

        self._chat_container = tk.Frame(self, bg="#fff")
        self._chat_container.pack(expand=1, fill='both')

        self._chat_history_container = self.__create_chat_history(self._chat_container)
        self._msg_box_container = self.__create_msg_box(self._chat_container)

    def __create_chat_history(self, parent):
        chat_history_container = tk.Frame(parent, bg='#fff')
        chat_history_container.pack(side="top", fill="x", pady=10, padx=15)

        for msg in self._chat_history:
            msg_label = tk.Label(chat_history_container, text=msg[1], font=("Arial", "10"))

            if msg[0] == self._userId:
                text_justify = 'w'
                msg_label.config(bg='green')
            
            msg_label.pack(pady=5, anchor=text_justify)

        return chat_history_container

    def __create_msg_box(self, parent):
        message_container = tk.Frame(parent)
        message_container.pack(side="bottom", fill="x", pady=10, padx=10)

        message_entry = tk.Entry(message_container)
        message_entry.config(font=("Arial", "8"))
        
        send_button = tk.Button(message_container, command=lambda: self.__send_message(message_entry))
        send_button.config(text="Enviar", font=("Arial", "7"), width=5, height=2)
        send_button.pack(side="right")

        message_entry.pack(side="right", padx=10, fill="x")

        return message_container

    def __send_message(self, msg_entry):
        #envia msg ao outro user
        msg = msg_entry.get()

        msg_label = tk.Label(self._chat_history_container, text=msg, font=("Arial", "10"))
        msg_label.pack(pady=5, anchor='e')

        self._chat_history.append((self._userId, msg))

        print(self._userId, msg)

    def add_user_msg(self, userId, msg):
        msg_label = tk.Label(self._chat_history_container, text=msg, font=("Arial", "10"), bg='green')
        msg_label.pack(pady=5, anchor='w')

        self._chat_history.append((userId, msg))

        print(userId, msg)