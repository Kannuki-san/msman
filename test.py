import os
import sys
import subprocess as spr
from subprocess import PIPE
import tkinter as tk
from tkinter.constants import CENTER

#window
window = tk.Tk()
window.title("serverconsole")

window.geometry('400x300')


proc = spr.run("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)
output = tk.Label(text=proc, width=50)
output.pack(anchor='center')


window.mainloop()