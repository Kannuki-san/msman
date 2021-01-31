import sys
from cx_Freeze import setup,Executable

base = None


# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'win32'


exe = Executable(script = 'tkmain.py',base = base)

setup(name = 'MSman',
      version = '0.1',
      description = 'converter',
      executables = [exe])