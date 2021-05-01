import tkinter as tk
from interface.initialScreen import InitialScreen
from interface.mainScreen import MainScreen

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('App bate-papo')
        self.config(background='#fff')
        self.geometry('750x500')
        self.resizable(False, False)

        self._frame = None
        self.switch_frame('MainScreen', 'teste')

    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = None

        if frame_class == 'InitialScreen' or len(args) == 0:
            new_frame = InitialScreen(self)
        elif frame_class == 'MainScreen' and len(args) > 0:
            new_frame = MainScreen(self, args[0])

        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.config(bg="#fff")
        self._frame.pack(expand=1, fill="both")