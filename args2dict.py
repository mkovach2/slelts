import re
texte='\n'
done = 0
try:
    while not(done):
        line = input("gib texte.  press enter twice to continue.\n")
        if re.match(line,r'[\n\r]{2,}'):
            done = 1
        texte += line + '\n'
    
    print(texte)

    step1 = r'(:[\s\w]+)?\s?=\s?'
    repl1 = r'" : '
    step2 = r'([\n\r]+)\s+'
    repl2 = r'\1"'
    texte = re.sub(step1,repl1,texte)
    print('\n')
    print(re.sub(step2,repl2,texte))
except Exception as ploop:
    print("FACK! uh oh!  u got:\t\t{}".format(ploop))


input('press enter to close lol\n')



#   regex backups:
    # step1 = r'(:[\s\w]+)?\s?=\s?'
    # repl1 = r'" : '
    # step2 = r'([\n\r]+)\s+'
    # repl2 = r'\1"'