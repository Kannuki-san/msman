#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.bubble import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget

Builder.load_file('MSman.kv')

class MyWidget(Widget):
    pass

class MScan(App):
    '''
    def __init__(self, **kwargs):
        super(MSman, self).__init__(**kwargs)
    '''
    def build(self):
        return MyWidget()




if __name__ == '__main__':
    MScan().run()