import tkinter as tk
from interface.chat import Chat
from interface.logIn import LogIn

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('App bate-papo')
        self.config(background='#fff')
        self.geometry('750x500')
        self.resizable(False, False)

        self._frame = None
        self.switch_frame(LogIn)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.config(bg="#fff")
        self._frame.pack(expand=1, fill="both")