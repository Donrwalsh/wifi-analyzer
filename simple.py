#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, RIGHT, BOTH, RAISED, W
from ttk import Frame, Button, Style, Label, Entry

#Currently has entry points and buttons, but they don't do anything and are on top of one another.

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("wifi-analyzer")
        self.style = Style()
        self.style.theme_use("default")
        self.centerWindow()

        MyButton1 = Button(self, text="BUTTON1", width=10)
        MyButton1.grid(row=0, column=0)

        MyButton2 = Button(self, text="BUTTON2", width=10)
        MyButton2.grid(row=0, column=1)

        MyButton3 = Button(self, text="BUTTON3", width=10)
        MyButton3.grid(row=0, column=2)

        Label(self, text="First").grid(row=0, sticky=W)
        Label(self, text="Second").grid(row=1, sticky=W)

        e1 = Entry(self)
        e2 = Entry(self)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        frame = Frame(self, relief=RAISED, borderwidth=1)


        self.pack(fill=BOTH, expand=True)

    def centerWindow(self):
        w = 400
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    root.geometry("350x200+300+300")
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()