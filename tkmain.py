import os
import tkinter as tk
from tkinter import Label, Toplevel, font
from tkinter.scrolledtext import ScrolledText
import subprocess
from tkinter.constants import DISABLED, END, OUTSIDE, RIGHT, TOP
import threading
import tkinter.filedialog
import configparser

class MSman(tk.Frame):
    output = ""
    config = configparser.ConfigParser()
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.readconfig()

    def create_widgets(self):
        self.console = tk.Frame(root)
        self.topbutton = tk.Frame(root)
        self.frame0 = tk.Frame(root)
        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        self.frame3 = tk.Frame(root)

        #topbutton
        self.SVstart = tk.Button(self.topbutton, text="start server", command=self.Start_Clicked)
        self.SVstart.grid(row=0, column=0, padx=10, pady=10)
        self.SVStop = tk.Button(self.topbutton, text="stop server", command=self.MSStop)
        self.SVStop.grid(row=0, column=1, padx=10, pady=10)
        self.quit = tk.Button(self.topbutton, text='QuitWindow', command=root.destroy)
        self.quit.grid(row=0, column=2, padx=10, pady=10)

        self.topbutton.pack(expand=True, fill='y', anchor='center', side=TOP, padx=10, pady=10)

        #console
        console_font = font.Font(root,family='MSゴシック')
        self.output = ScrolledText(self.console,background='black',fg='white',font=console_font)
        self.output.pack(padx=10, pady=10,fill='both')
        self.console.pack(expand=True, fill="both",side=RIGHT)

        #menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        File = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='files',menu=File)
        File.add_command(label='OpenServer',command=self.Open_Serverfile)
        File.add_command(label='OpenDirectory',command=self.Setdir)
        File.add_command(label='Settings',command=self.settings)
        


    serverplace = ''
    Serverdir = ''


    def Start_Clicked(self):
        self.thread1 = threading.Thread(target=self.StartMS)
        self.thread1.start()

    def StartMS(self):
        logbuf = ""
        if self.Serverdir:
            if '.jar' in self.serverplace:
                for output_line in self.MServer(cmd='java -jar '+self.serverplace+' nogui'):
                    if output_line != logbuf:
                        line1 = str(output_line)[2:]
                        line2=line1[::-1]
                        line=line2[2:]
                        self.output.insert(tk.END,output_line+'\n')
                        self.output.see(tk.END)
                        logbuf = output_line

            else:
                self.output.insert(tk.END,'サーバーファイルが選択されていません\n')
                self.output.see(tk.END)
        else:
                self.output.insert(tk.END,'サーバーディレクトリが選択されていません\n')
                self.output.see(tk.END)
                
        '''
                await self.output.insert(tk.END,output_line)
                await self.output.insert(tk.END,'\n')
                await self.output.see(tk.END)
        '''

    def MServer(self,cmd):
        self.p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,text=True,cwd=self.Serverdir)
        stdout_data = self.p.stdout.readline
        return iter(stdout_data,None)
        #("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    


    def MSStop(self):
        self.p.stdin.write('stop\n')
        self.p.stdin.flush()
        

    def Logstop(self):
        False
    
    '''async def Logging(self):
        logbuffer = "default"
        while True:
            if logbuffer != self.line:
                logbuffer = self.line
                self.output.insert(self.line,'\n')
                self.output.see('end')
            if self.Logstop == True:
                break
    '''

    def Open_Serverfile(self):
        self.serverplace = tkinter.filedialog.askopenfilename(filetypes=[('Serverfile','*.jar')])
        self.filepath['text']=self.serverplace

    def Setdir(self):
        self.Serverdir = tkinter.filedialog.askdirectory()
        self.dir_path['text']=self.Serverdir

    def settings(self):
        sub_win = Toplevel(master=self.master)
        setting_t = tk.Label(sub_win,text='設定')
        setting_t.pack()
        file = tk.Label(sub_win,text='サーバーファイル')
        file.place(x=8,y=40)
        self.filepath=tk.Label(sub_win,text=self.serverplace,background='#dddddd',width=34)
        self.filepath.place(x=90,y=40)
        file_button = tk.Button(sub_win,text='参照',command=self.Open_Serverfile)
        file_button.place(x=350,y=38)
        direc = tk.Label(sub_win,text='サーバーフォルダ')
        direc.place(x=8,y=70)
        self.dir_path=tk.Label(sub_win,text=self.Serverdir,background='#dddddd',width=34)
        self.dir_path.place(x=90,y=70)
        dir_button = tk.Button(sub_win,text='参照',command=self.Setdir)
        dir_button.place(x=350,y=68)
        Decision=tk.Button(sub_win,text='保存',command=self.setconfig)
        Decision.place(x=350,y=250)
        setting_t.focus_set()
        sub_win.transient(self.master)
        sub_win.grab_set()
        sub_win.geometry('400x300')
        
        sub_win.resizable(width=False, height=False)



    def readconfig(self):
        self.config.read('config.ini')
        if os.path.isfile('config.ini') == False:
            self.setconfig()
        read_Files = self.config['Files']
        self.serverplace = read_Files.get('Serverfile')
        self.Serverdir = read_Files.get('ServerDir')
    
    def setconfig(self):
        self.config['Files'] = {
            'Serverfile':self.serverplace,
            'ServerDir' :self.Serverdir,
            }
        with open('config.ini','w') as file:
            self.config.write(file)

    def quit(self):
        self.config['Files'] = {
            'Serverfile':self.serverplace,
            'ServerDir' :self.Serverdir,
            }
        with open('config.ini','w') as file:
            self.config.write(file)
        self.p.stdin.write('stop\n')
        self.p.stdin.flush()
        self.thread1.join()
        root.destroy()

    
        


root = tk.Tk()
app = MSman(master=root)
root.title('MSman')
app.mainloop()