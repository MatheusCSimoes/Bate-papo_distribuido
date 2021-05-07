import tkinter as tk
from user import User

class InitialScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        self.logIn_container = tk.Frame(self, bg="#fff")
        self.logIn_container.pack(expand=1, anchor=tk.CENTER)

        self.username_container = tk.Frame(self.logIn_container, bg="#fff")
        self.username_container.pack(side="top", pady=10)

        self.username_label = tk.Label(self.username_container, text="Username:", font=("Arial", "10"), bg="#fff")
        self.username_label.pack(side="left", padx=3)

        self.username_entry = tk.Entry(self.username_container)
        self.username_entry.config(font=("Arial", "10"), width=30)
        self.username_entry.pack(side="right", padx=3)

        self.button_container = tk.Frame(self.logIn_container)
        self.button_container.pack(side="bottom")

        self.connect_button = tk.Button(self.button_container, command=lambda: self._connectUser(master))
        self.connect_button.config(text="Conectar", font=("Arial", "10"), width=10)
        self.connect_button.pack()

        self.user = None

    def _connectUser(self, master):
        username = self.username_entry.get()

        #valida nome (apenas caracteres e numeros)

        self.user = User(username)

        if self.user.connect(username):
            self.user.getActiveUsers()
            master.switch_frame('MainScreen', self.user)