#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup,Executable

icondata='icon.ico'


base = None

# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'win32GUI'


exe = Executable(script = 'main.py',base = base ,icon = icondata)


setup(name = 'MSman',
      version = '0.1',
      description = 'converter',
      executables = [exe])