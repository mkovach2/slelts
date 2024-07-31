import re

again = 'y'

step1 = r'[\"\']\s?:\s?'
repl1 = r' = '
step2 = r'\s+[\'\"]?'
repl2 = r''

while again.lower() == 'y':
    
    texte = '\n'
    done = 0
    
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
                texte_nn = re.sub(step2,repl2,texte_nn)
                texte_nn = texte_nn.replace('\\(','(')
                texte_nn = texte_nn.replace('\\)',')')
                texte_nn = texte_nn.replace('\\*','*')
                
                if texte_nn[-1] != ',':
                    texte_nn += ','
                
                print(f'{texte_nn.strip()}')
    
    except Exception as ploop:
        print("FACK! uh oh!  u got:\t\t{}".format(ploop))
    
    done = 0
    again = input('again (y/N)?\t')



#   regex backups:
# step1 = r'[\"\']\s?:\s?'
# repl1 = r' = '
