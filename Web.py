#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import PyQt5.QtWidgets
import sys
import os
import urllib.request
#import threading

class Downloader(PyQt5.QtWidgets.QWidget):
    
    def __init__(self) -> PyQt5.QtWidgets:
        super().__init__()

        self.browser()

    def browser(self):
        URL = 'https://www.minecraft.net/ja-jp/download/server/'

        PyQt5.QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(
            self.on_downloadRequested
        )

        self.browser = QWebEngineView()
        self.browser.load(QUrl(URL))
        self.browser.resize(800,600)
        self.browser.move(200,200)
        self.browser.setWindowTitle('Minecraft')
        self.progressBar = PyQt5.QtWidgets.QProgressBar(self) 
        grid = PyQt5.QtWidgets.QGridLayout()
        grid.addWidget(self.browser,2, 0, 5, 15)
        grid.addWidget(self.progressBar)
        self.setLayout(grid) 
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('Minecraft')
        self.show()

    def center(self):
        ''' centering widget
        '''
        qr = self.frameGeometry()
        cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


        
    @PyQt5.QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self,download):
        self.old_path = download.url().path()  # download.path()
        #self.thread = threading.Thread(target=self.download)
        #self.thread.setDaemon(True)
        #self.thread.start()
        #self.thread.join()
        self.download()
        
    def check(self, block_count, block_size, total_size):
        percentage = 100.0 * block_count * block_size / total_size
        self.progressBar.setValue(percentage) 
        PyQt5.QtWidgets.QApplication.processEvents()

    
    def download(self):
        if not os.path.isdir('./ServerData'):
            os.mkdir('./ServerData')
        else:subwindow().show('すでにフォルダがあります')
        if not os.path.isfile('./ServerData/server.jar'):
            urllib.request.urlretrieve('https://launcher.mojang.com'+self.old_path,'./ServerData/server.jar',self.check) #'https://launcher.mojang.com'+self.old_path
            #https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar
            subwindow().show('ダウンロードが完了しました')
        else:subwindow().show('すでにファイルがあります')

class subwindow(PyQt5.QtWidgets.QWidget):
    text = '完了'
    def __init__(self,parent = None):
        super().__init__()
        self.w = PyQt5.QtWidgets.QDialog(parent)
        self.label = PyQt5.QtWidgets.QLabel()
        self.label.setText(self.text)
        button = PyQt5.QtWidgets.QPushButton('閉じる',self.w)
        button.clicked.connect(sys.exit)
        layout = PyQt5.QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.w.setLayout(layout)

        
    
    def show(self,text):
        self.label.setText = text
        self.w.exec_()

    

def run():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = Downloader()
    sys.exit(app.exec_())

if __name__ == '__main__':
        # mainPyQt5()
    app = PyQt5.QtWidgets.QApplication(sys.argv)

    # setWindowIcon is a method for QApplication, not for QWidget

    ex = Downloader()
    sys.exit(app.exec_())
