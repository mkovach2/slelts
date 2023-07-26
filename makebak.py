# makebak.py
import shutil

inputStr = 'input path to original file:\n'
original = input(inputStr).replace("\\","/").strip('\"')
try:
    shutil.copy(original,original + '.bak')
    bad = 0
except Exception as ooo:
    print(ooo)
    bad = 1
if not(bad):
    outStr = 'done.  backup saved as\n' + original + '.bak\n' +\
        'press enter to close.\n'
    input(outStr)
else:
    input('\npress enter to close.\n')
