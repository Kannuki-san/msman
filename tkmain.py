import tkinter as tk

class MSman(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text='Hello World', width=50)
        self.title.pack(anchor='center')
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="bottom")


root = tk.Tk()
app = MSman(master=root)
root.title('Minecraft Server Manager')
app.mainloop()