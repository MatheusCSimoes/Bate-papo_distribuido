import tkinter as tk

class Chat(tk.Frame):
    def __init__(self, master, user, userId, userName):
        tk.Frame.__init__(self, master)
        self._userId = userId
        self._userName = userName
        self._chat_history = []
        
        self._user = user

        self._chat_container = tk.Frame(self, bg="#fff")
        self._chat_container.pack(expand=1, fill='both')

        self._chat_history_container = self._create_chat_history(self._chat_container)
        self._msg_box_container, self._send_button = self._create_msg_box(self._chat_container)

    def _create_chat_history(self, parent):
        chat_history_container = tk.Frame(parent, bg='#fff')
        chat_history_container.pack(side="top", fill="x", pady=10, padx=15)

        for msg in self._chat_history:
            msg_label = tk.Label(chat_history_container, text=msg[1], font=("Arial", "10"))

            text_justify = 'e'
            if msg[0] == self._userId:
                text_justify = 'w'
                msg_label.config(bg='#8ef589')
            
            msg_label.pack(pady=5, anchor=text_justify)

        return chat_history_container

    def _create_msg_box(self, parent):
        message_container = tk.Frame(parent)
        message_container.pack(side="bottom", fill="x", pady=10, padx=10)

        message_entry = tk.Entry(message_container)
        message_entry.config(font=("Arial", "8"))
        
        send_button = tk.Button(message_container, command=lambda: self._send_message(message_entry))
        send_button.config(text="Enviar", font=("Arial", "7"), width=5, height=2)
        send_button.pack(side="right")

        message_entry.pack(side="right", padx=10, expand=1, fill="x")

        return message_container, send_button

    def _send_message(self, msg_entry):
        #envia msg ao outro user
        msg = msg_entry.get()  
        msg_max_width = self._chat_history_container.winfo_width()

        if self._user.sendMsgToUser(self._userId, msg):
            msg_label = tk.Label(self._chat_history_container, text=msg, font=("Arial", "10"), wraplength=msg_max_width, justify='left')
            msg_label.pack(pady=5, anchor='e')
            self._chat_history.append((self._userId, msg))
        
            msg_entry.delete(0, 'end')
        else:
            print('erro ao enviar msg')

    def add_user_msg(self, userId, msg):
        msg_max_width = self._chat_history_container.winfo_width()
        if msg_max_width < 10:
            msg_max_width = 500

        msg_label = tk.Label(self._chat_history_container, text=msg, font=("Arial", "10"), bg='#8ef589', wraplength=msg_max_width, justify='left')
        msg_label.pack(pady=5, anchor='w')

        self._chat_history.append((userId, msg))

    def updateStatus(self, active):
        if active == 0:
            self._send_button.config(state='disabled')
        else:
            self._send_button.config(state='normal')