import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
from subprocess import CREATE_BREAKAWAY_FROM_JOB, PIPE
import asyncio
from tkinter.constants import END, OUTSIDE, RIGHT, TOP
import sys
import time
import threading

class MSman(tk.Frame):
    output = ""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.Logging()

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
        
        self.output = ScrolledText(self.console)
        self.output.pack(padx=10, pady=10)
        self.console.pack(expand=True, fill="both",side=RIGHT)



    def MServer(self,cmd):
        proc = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

        while True:
            self.line = proc.stdout.readline()
            if self.line:
                yield self.line

            if not self.line and proc.poll() is not None:
                break
        #("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)

    def MSStop(self):
        None

    def Logstop():
        False
    
    async def Logging(self):
        logbuffer = "default"
        while True:
            if logbuffer != self.line:
                logbuffer = self.line
                self.output.insert(self.line,'\n')
                self.output.see('end')
            if self.Logstop == True:
                break



root = tk.Tk()
app = MSman(master=root)
root.title('Minecraft Server Manager')
app.mainloop()