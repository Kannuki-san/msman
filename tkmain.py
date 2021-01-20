import tkinter as tk
import subprocess
from subprocess import CREATE_BREAKAWAY_FROM_JOB, PIPE
import asyncio
from tkinter.constants import OUTSIDE

class MSman(tk.Frame):
    output = ""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text='Hello World', width=50)
        self.title.pack(anchor='center', expand=False, fill='x')
        self.MStart = tk.Button(self, text="start", fg="green", command=self.MServer)
        self.MStart.pack(anchor='center', expand=False, fill='x')
        self.title = tk.Label(self, text=self.output, width=50)
        self.title.pack(anchor='center', expand=False, fill='x')
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="bottom", expand=False, fill='x')

    async def MServer(self):
        self.output = subprocess.Popen("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)

root = tk.Tk()
app = MSman(master=root)
root.title('Minecraft Server Manager')
app.mainloop()