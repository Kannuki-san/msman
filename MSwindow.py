import tkinter as tk


def create_widgets(output,cm):
    title = tk.Label(text='Hello World', width=50)
    title.pack(anchor='center', expand=False, fill='x')
    MStart = tk.Button(text="start", fg="green", command=cm)
    MStart.pack(anchor='center', expand=False, fill='x')
    title = tk.Label(text=output, width=50)
    title.pack(anchor='center', expand=False, fill='x')
    quit = tk.Button(text="QUIT", fg="red",command=cm)
    quit.pack(side="bottom", expand=False, fill='x')

    return 
