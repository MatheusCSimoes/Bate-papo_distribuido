import tkinter as tk
from interface.application import Application

app = None

def on_closing():
    app.close_window()
    app.destroy()


def main():
    global app 
    app = Application()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == '__main__':
    main()