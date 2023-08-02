# makebak.py
import shutil

input_prompt = 'input path to original file:\n'
inputStr = input(input_prompt)
while inputStr != '':
    original = inputStr.replace("\\","/").strip('\"')
    try:
        shutil.copy(original,original + '.bak')
        bad = 0
    except Exception as ooo:
        print(ooo)
        bad = 1
    if not(bad):
        outStr = 'done.  backup saved as\n\n' + original + '.bak\n\n' +\
            'input another file to continue, or press enter to close.\n'
        inputStr = input(outStr)
    else:
        input('\npress enter to close.\n')
        inputStr = ''
