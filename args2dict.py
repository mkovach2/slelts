import re

winCmd = True

texte='\n'
done = 0

step1 = r'(:[\s\w]+)?\s?=\s?'
repl1 = r'" : '
step2 = r'([\n\r]+)\s+'
repl2 = r'\1"'

try:
    while not(done):
        line = input("gib texte.  press enter twice to continue.\n")
        # you have to do this bonanzo garbage bc otherwise re thinks 
        # parens and asterisks are a pattern??
        line = line.replace('(','\(')
        line = line.replace(')','\)')
        line = line.replace('*','\*')
        
        if re.match(line,r'[\n\r]{2,}'):
            done = 1
        texte += line + '\n'
    
    print(f'texte = {texte}')
    texte = texte.split('\n')
    
    for texte_nn in texte:
        if texte_nn != '':
            texte_nn = re.sub(step1,repl1,texte_nn,count = 1)
            # print('\n')
            texte_nn = re.sub(step2,repl2,texte_nn)
            texte_nn = texte_nn.replace('\\(','(')
            texte_nn = texte_nn.replace('\\)',')')
            texte_nn = texte_nn.replace('\\*','*')
            print(f'\"{texte_nn}')

except Exception as ploop:
    print("FACK! uh oh!  u got:\t\t{}".format(ploop))


if winCmd == True:
    input('press enter to close lol\n')



#   regex backups:
    # step1 = r'(:[\s\w]+)?\s?=\s?'
    # repl1 = r'" : '
    # step2 = r'([\n\r]+)\s+'
    # repl2 = r'\1"'