import os
import sys
import tkinter.font as font
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
from tkinter.constants import DISABLED, END, OUTSIDE, RIGHT, TOP
import threading
import tkinter.filedialog
import configparser
import datetime
import tkinter.ttk as ttk
import linecache

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
        self.underbox = tk.Frame(root)
        self.frame0 = tk.Frame(root)
        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        self.frame3 = tk.Frame(root)

        #topbutton
        self.SVstart = tk.Button(self.topbutton, text="start server", command=self.Start_Clicked)
        self.SVstart.grid(row=0, column=0, padx=10, pady=10)
        self.SVStop = tk.Button(self.topbutton, text="stop server", command=self.MSStop)
        self.SVStop.grid(row=0, column=1, padx=10, pady=10)
        self.quit = tk.Button(self.topbutton, text='QuitWindow', command=self.quit)
        self.quit.grid(row=0, column=2, padx=10, pady=10)

        self.topbutton.pack(expand=False, side='top', padx=10, pady=10)

        #console
        console_font = font.Font(root,family='MSゴシック')
        self.output = ScrolledText(self.console,background='black',fg='white',font=console_font)
        self.output.pack(padx=10, pady=10,fill='both',expand=True)
        self.console.pack(expand=True, fill="both")

        #menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        File = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='files',menu=File)
        File.add_command(label='OpenServer',command=self.Open_Serverfile)
        File.add_command(label='OpenDirectory',command=self.Setdir)
        File.add_command(label='Settings',command=self.settings)

        #textbox
        self.commandbox = tk.Entry(self.underbox)
        self.commandbox.pack(padx=5,pady=5,fill='x')
        self.commandbox.bind('<Return>',self.write_mconsole)
        self.underbox.pack(expand=False,fill='x',side='bottom')
        


    serverplace = ''
    Serverdir = ''


    def Start_Clicked(self):
        if self.Serverdir:
            if '.jar' in self.serverplace:
                if self.check_eula():
                    self.thread1 = threading.Thread(target=self.StartMS)
                    self.thread1.setDaemon(True)
                    self.thread1.start()
                else:
                    self.sign_eula()
            else:
                self.output.insert(tk.END,'サーバーファイルが選択されていません\n')
                self.output.see(tk.END)
        else:
            self.output.insert(tk.END,'サーバーディレクトリが選択されていません\n')
            self.output.see(tk.END)
    
    def StartMS(self):
        logbuf = ""
        for output_line in self.MServer(cmd='java -server '+self.serverMem+'-jar' +self.serverplace+ ' nogui'):
                if output_line != logbuf:
                    self.output.insert(tk.END,output_line)
                    self.output.see(tk.END)
                    logbuf = output_line


                

    def MServer(self,cmd):
        
        self.p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,cwd=self.Serverdir,text=True)
        stdout_data = self.p.stdout.readline
        return iter(stdout_data,None)
        #("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    


    def MSStop(self):
        if hasattr(self,'p'):
            self.p.stdin.write('stop\n')
            self.p.stdin.flush()
            delattr(self,'p')
        

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
        sub_win = tk.Toplevel(master=self.master)
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
        Getmodlist = tk.Button(sub_win,text='Modlist取得',command=self.get_mods)
        Getmodlist.place(x=8,y=100)
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
        read_SC = self.config['ServerConfig']
        self.serverMem = read_SC.get('Memory')
        self.Addop = read_SC.get('addition')
    
    def setconfig(self):
        self.config['Files'] = {
            'Serverfile':self.serverplace,
            'ServerDir' :self.Serverdir,
            }
        self.config['ServerConfig']={
            'Memory' :self.serverMem,
            'addition':self.Addop
        }
        with open('config.ini','w',encoding='utf-8') as file:
            self.config.write(file)

    def quit(self):
        if hasattr(self,'p'):
            self.output.insert(tk.END,'サーバーが開いています\n')
            self.output.see(tk.END)

        else:    
            self.setconfig()
            root.destroy()

    def check_eula(self):
        if os.path.isfile(self.Serverdir +'/eula.txt'):
            eula_line = linecache.getline(self.Serverdir +'/eula.txt',int(3))
            print(eula_line)
            text = 'eula=true\n'
            print(text)
            if eula_line == text:
                linecache.clearcache()
                return True
            else:
                linecache.clearcache()
                return False
        else:
            return False

    def sign_eula(self):
        self.eula_win = tk.Toplevel(master=self.master)
        label1=tk.Label(self.eula_win,text='trueに設定することで、EULA(https://account.mojang.com/documents/minecraft_eula)を承諾できます。')
        label1.pack()
        self.ebox = ttk.Entry(self.eula_win)
        self.ebox.pack()
        button = tk.Button(self.eula_win,text='OK',command=self.write_eula)
        button.pack()
        self.eula_win.focus_set()
        self.eula_win.transient(self.master)
        self.eula_win.grab_set()

    def write_eula(self):
        if self.ebox.get() == 'true':
            self.eula_win.destroy
            path=self.Serverdir +'/eula.txt'
            f = open(path, 'w')
            today = datetime.date.today()
            text='#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).'
            f.write(text + '\n' +str(today)+ '\n' + 'eula=true')
            f.close

    def get_mods(self):
        isdir = os.path.isdir(self.Serverdir+'/mods')
        if isdir:
            mods = os.listdir(self.Serverdir+'/mods')
            with open('modlist.txt','w',encoding='utf-8') as modlist:
                modlist.write('mod一覧\n')
                list = '\n'.join(mods)
                modlist.write(list)
                modlist.close()

    def write_mconsole(self,event):
        if hasattr(self,'p'):
            command = str(self.commandbox.get())
            self.commandbox.delete(0, tk.END)
            self.p.stdin.write(command+'\n')
            self.p.stdin.flush()
        else:
            self.output.insert(tk.END,'サーバーはまだ動作していません\n')
            self.output.see(tk.END)
            self.commandbox.delete(0, tk.END)

                    
    
    


root = tk.Tk()
app = MSman(master=root)
root.title('MSman')
app.mainloop()