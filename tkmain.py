from os import truncate
import tkinter as tk
import subprocess
from subprocess import CREATE_BREAKAWAY_FROM_JOB, PIPE
import asyncio
from tkinter.constants import OUTSIDE, RIGHT, TOP
import sys
import time
import threading

class MSman(tk.Frame):
    output = ""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.console = tk.Frame(root)
        self.topbutton = tk.Frame(root)
        self.frame0 = tk.Frame(root)
        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        self.frame3 = tk.Frame(root)

        #topbutton
        self.SVstart = tk.Button(self.topbutton, text="start server", command=self.MServer())
        self.SVstart.grid(row=0, column=0, padx=10, pady=10)
        self.SVStop = tk.Button(self.topbutton, text="stop server", command=self.MSStop())
        self.SVStop.grid(row=0, column=1, padx=10, pady=10)
        self.quit = tk.Button(self.topbutton, text='QuitWindow', command=root.destroy)
        self.quit.grid(row=0, column=2, padx=10, pady=10)

        self.topbutton.pack(expand=True, fill='both', anchor='center', side=TOP, padx=10, pady=10)

        #console
        
        self.output = scrolledtext(self.console)
        self.output.pack()
        self.console.pack(expand=True, fill="both",side=RIGHT)



    def MServer(self):
        self.output = subprocess.Popen("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)

    def MSStop(self):
        None


root = tk.Tk()
app = MSman(master=root)
root.title('Minecraft Server Manager')
app.mainloop()