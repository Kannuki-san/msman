#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup,Executable

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


base = None


# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'win32GUI'


exe = Executable(script = 'main.py',base = base ,icon = icondata,)


setup(name = 'MSman',
      version = '0.1',
      description = 'converter',
      executables = [exe])