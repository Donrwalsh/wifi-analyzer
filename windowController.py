#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import Queue
from Tkinter import *
import ttk
from ttk import Frame, Button, Style, Label, Entry
import Tkinter

#Currently opens a non-working progress bar with the 'go' button.

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("wifi-analyzer")
        self.pack(fill=BOTH, expand=True)
        self.centerWindow()

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=500, mode='indeterminate')

        self.hbtn = Button(self, text="Help")
        self.hbtn.grid(row=5, column=0, padx=5)

        self.gbtn = Button(self, text="Go", command=self.go)
        self.gbtn.grid(row=5, column=3)

    def go(self):
        self.progress.grid(row=3, column=1)
        self.progress.start(50)
        self.gbtn['state'] = 'disabled'

    def centerWindow(self):
        w = 400
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tkinter.Tk()
    root.geometry("350x200+300+300")
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()

