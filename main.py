#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter.font as font
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
from tkinter.constants import DISABLED, END, HORIZONTAL, OUTSIDE, RIGHT, TOP, UNDERLINE
import threading
import tkinter.filedialog
import configparser
import datetime
import tkinter.ttk as ttk
import linecache
import Web
import requests
import socket

#from mcstatus import MinecraftServer

class MSman(tk.Frame):
    output = ""
    config = configparser.ConfigParser()
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.setfirst()
        self.readconfig()
        self.create_widgets()

    def create_widgets(self):
        self.console = tk.Frame(root)
        self.topbutton = tk.Frame(root)
        self.underbox = tk.Frame(root)
        self.address = tk.Frame(root)
        #self.online_player = tk.Frame(root)
        #self.frame0 = tk.Frame(root)
        #self.frame1 = tk.Frame(root)
        #self.frame2 = tk.Frame(root)
        #self.frame3 = tk.Frame(root)

        #topbutton
        self.SVstart = tk.Button(self.topbutton, text="サーバー起動", command=self.Start_Clicked)
        self.SVstart.grid(row=0, column=0, padx=10, pady=10)
        self.Save = tk.Button(self.topbutton,text='セーブワールド', command=self.SAVE)
        self.Save.grid(row=0, column=1, padx=10, pady=10)
        self.SVStop = tk.Button(self.topbutton, text="サーバー停止", command=self.MSStop)
        self.SVStop.grid(row=0, column=2, padx=10, pady=10)
        self.GetServer = tk.Button(self.topbutton,text='公式サーバーをダウンロード',command=self.Get_Server)
        self.GetServer.grid(row=0,column=3,padx=10, pady=10)
        self.quit = tk.Button(self.topbutton, text='終了', command=self.quit)
        self.quit.grid(row=0, column=4, padx=10, pady=10)


        self.topbutton.pack(expand=False, side='top', padx=10, pady=10)
        
        self.IP = tk.Label(self.address)
        self.IP.pack(padx=10, pady=10)

        self.address.pack(expand=False, side='top', padx=10, pady=10)
        
        '''
        #player
        self.playerlist = tk.Label(self.online_player,text='オンライン{0}人'.format(self.status))
        self.playerlist.pack()
        self.online_player.pack()
        '''

        #console
        console_font = font.Font(root,family='MSゴシック')
        self.output = ScrolledText(self.console,background='black',fg='white',font=console_font)
        self.output.pack(padx=10, pady=10,fill='both',expand=True)
        self.output.configure(state='disabled')
        self.console.pack(expand=True, fill="both")

        #menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        File = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='ファイル',menu=File)
        File.add_command(label='サーバーファイル',command=self.Open_Serverfile)
        File.add_command(label='ディレクトリ',command=self.Setdir)
        File.add_command(label='設定',command=self.settings)

        #textbox
        self.commandbox = tk.Entry(self.underbox)
        self.commandbox.pack(padx=5,pady=5,fill='x')
        self.commandbox.bind('<Return>',self.write_mconsole)
        self.underbox.pack(expand=False,fill='x',side='bottom')



    def setfirst(self):
        self.serverplace = ''
        self.Serverdir = ''
        self.serverMem = '4'
        self.Addop=''
        self.status = 0
        self.StopConsole = False

    '''    
    def check_player(self):
        self.timestop == False
        self.server = MinecraftServer.lookup('localhost:25565')
        self.status = self.server.status()
        while not self.timestop:
            time.sleep(5)
            self.status = self.server.status()
            self.playerlist.config(text='aaaa')
    '''

    def Get_Server(self):
        #thread = threading.Thread(target=Web.run,daemon=True)
        #thread.start()
        #thread.join()
        cwd = os.getcwd()
        place = '/ServerData/server.jar'
        dir = '/ServerData'
        self.serverplace = cwd + str(place)
        self.Serverdir = cwd + str(dir)
        Web.run()




    def Start_Clicked(self):
        if self.Serverdir:
            if '.jar' in self.serverplace:
                if self.check_eula():
                    #self.check_word()
                    self.thread1 = threading.Thread(target=self.StartMS)
                    self.thread1.setDaemon(True)
                    self.thread1.start()
                    res = requests.get('http://inet-ip.info/ip')
                    ip = str(res.text.rstrip('\n'))
                    local = socket.gethostbyname(socket.gethostname())
                    self.propaties = configparser.ConfigParser()
                    port = ''
                    if os.path.isfile(self.Serverdir+'/server.properties'):
                        with open(self.Serverdir+'/server.properties','r', encoding="utf_8") as f:
                            line = f.readlines()
                            read = [s for s in line if 'query.port=' in s]
                            port = str(read).split('=')[1]
                            port = port[:-4]
                            f.close()
                    else:
                        port = 25565
                    self.IP['text'] = f'グローバルIP : {ip}\nローカルIP : {local}\nポート : {port}'

                else:
                    self.sign_eula()
            else:
                self.insert_line('サーバーファイルが選択されていません\n')
        else:
            self.insert_line('サーバーディレクトリが選択されていません\n')
    
    def StartMS(self):
        self.insert_line('少しお待ちください\n')
        for self.output_line in self.MServer(cmd='java -server '+ f'-Xmx{self.serverMem}G -Xms{self.serverMem}G '+self.Addop+' -jar ' +self.serverplace+ ' nogui'):
            self.insert_line(self.output_line)

            if self.StopConsole == True:
                self.insert_line('サーバーが停止しました\n')
                self.StopConsole = False
                break



    '''
    def check_word(self):
        for check in self.output_line:
            if 'help' in check:
                self.check_player()
    '''


    def insert_line(self,text):
        self.output.configure(state='normal')
        self.output.insert(tk.END,text)
        self.output.see(tk.END)
        self.output.configure(state='disabled')


                

    def MServer(self,cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        self.p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,cwd=self.Serverdir,text=True,startupinfo=startupinfo,shell=False)
        stdout_data = self.p.stdout.readline
        
        return iter(stdout_data,None)
        #("java -jar mohist-1.12.2-165-server.jar", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    


    def MSStop(self):
        if hasattr(self,'p'):
            self.p.stdin.write('stop\n')
            self.p.stdin.flush()
            self.StopConsole = True
            delattr(self,'p')
        else:
            self.insert_line('サーバーが開かれていません\n')

    def SAVE(self):
        if hasattr(self,'p'):
            self.p.stdin.write('save-all\n')
            self.p.stdin.flush()
        else:
            self.insert_line('サーバーが開かれていません\n')


        
    '''
    def Logstop(self):
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
    '''

    def Open_Serverfile(self):
        self.serverplace = tkinter.filedialog.askopenfilename(filetypes=[('Serverfile','*.jar')])

    def Setdir(self):
        self.Serverdir = tkinter.filedialog.askdirectory()

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
        Getmodlist.place(x=8,y=200)
        Mem = tk.Label(sub_win,text='割り当てメモリ')
        Mem.place(x=8, y=100)
        getMem = tk.Entry(sub_win)
        getMem.insert(tk.END,self.serverMem)
        GB = tk.Label(sub_win,text='GB')
        GB.place(x=200, y=100)
        getMem.place(x=90, y= 100)
        self.filepath['text']=self.serverplace
        self.dir_path['text']=self.Serverdir
        
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
        read_SC = self.config['Argument']
        self.serverMem = read_SC.get('Memory')
        self.Addop = read_SC.get('addition')
    
    def setconfig(self):
        self.config['Files'] = {
            'Serverfile':self.serverplace,
            'ServerDir' :self.Serverdir
        }
        self.config['Argument'] = {
            'Memory' :self.serverMem,
            'Addition' :self.Addop
        }
        with open('config.ini','w',encoding='utf-8') as file:
            self.config.write(file)

    def quit(self):
        if hasattr(self,'p') == True:
            self.MSStop()
        self.setconfig()
        root.destroy()

    def check_eula(self):
        if os.path.isfile(self.Serverdir +'/eula.txt'):
            eula_line = linecache.getline(self.Serverdir +'/eula.txt',int(3))
            text = 'eula=true\n'
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
            self.eula_win.destroy()

    def get_mods(self):
        isdir = os.path.isdir(self.Serverdir+'/mods')
        if isdir:
            mods = os.listdir(self.Serverdir+'/mods')
            with open('modlist.txt','w',encoding='utf-8') as modlist:
                modlist.write('mod一覧\n\n')
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
            self.insert_line('サーバーはまだ動作していません\n')
            self.commandbox.delete(0, tk.END)



icondata='''R0lGODlhEAAQAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr
/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCq
mQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMA
MzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV
/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPV
mTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYr
M2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA
/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/
mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlV
M5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq
/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswA
mcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyA
M8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV
/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8r
mf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+q
M/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP//
/wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAQABAAAAiyAPcJHFjHDbSBCBEqy5Bh
SAYNnxIOdJOByBANFhm+OShwYcWKDi0SYUhk35uGGoaMVDKyZQYe9TKF/JCRSJKU
Q3pQ0SeMl5uLIYH2IERIi7JhtXhJajNSQ8MzWrSA0UIv0y5Gu3jZuuQGTFFCXo0q
VbpLki1eURVpUatlGC9eWRnBlVTU69S2whhJyhqJFyO7WooK28crUlJJhdGG1aJw
2KKkSgNrwSSxo6THUStLPFo5IAA7
'''
root = tk.Tk()
root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(data=icondata))
app = MSman(master=root)
root.title('MSman')
app.mainloop()