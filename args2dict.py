import re

again = 'y'

step1 = r'(:[\s\w]+)?\s?=\s?'
repl1 = r'" : '
step2 = r'([\n\r]+)\s+'
repl2 = r'\1"'
two_enters = r'[\n\r]{2,}'

comment_char = '#'

while again.lower() == 'y':
    
    texte = '\n'
    done = 0
    
    try:
        while not(done):
            line = input("gib texte.  press enter twice to continue.\n")
            # you have to do this bonanzo garbage bc otherwise re thinks 
            # parens and asterisks are a pattern??
            line = line.replace('(','\\(')
            line = line.replace(')','\\)')
            line = line.replace('*','\\*')
            
            if re.match(line, two_enters):
                done = 1
            texte += line + '\n'
        
        print(f'texte = {texte}')
        texte = texte.split('\n')
        
        for texte_nn in texte:
            texte_nn_split = list(texte_nn.rpartition(comment_char)) # look for comments
            # print(texte_nn_split)
            
            # line_blank = False
            if texte_nn_split[1] == comment_char or texte_nn_split[-1] != '':
                if texte_nn_split[0] == '':
                    tnn = 2
                else:
                    tnn = 0
                
                texte_nn_split[tnn] = texte_nn_split[tnn].rstrip()
                
                texte_nn_split[tnn] = re.sub(step1,repl1,texte_nn_split[tnn],count = 1)
                texte_nn_split[tnn] = re.sub(step2,repl2,texte_nn_split[tnn])
                
                texte_nn_split[tnn] = texte_nn_split[tnn].replace('\\(','(')
                texte_nn_split[tnn] = texte_nn_split[tnn].replace('\\)',')')
                texte_nn_split[tnn] = texte_nn_split[tnn].replace('\\*','*')
                
                texte_nn_split[tnn] = '\"' + texte_nn_split[tnn].strip()
                
                if texte_nn_split[tnn][-1] != ',':
                    texte_nn_split[tnn] += ', '
                
                texte_nn = ''.join(texte_nn_split)
                print(texte_nn)
    
    except Exception as ploop:
        print("FACK! uh oh!  u got:\t\t{}".format(ploop))
    
    done = 0
    again = input('again (y/N)?\t')

input("\ndone.  press [enter] to close.\n_")

#   regex backups:
    # step1 = r'(:[\s\w]+)?\s?=\s?'
    # repl1 = r'" : '
    # step2 = r'([\n\r]+)\s+'
    # repl2 = r'\1"'
    # two_enters = r'[\n\r]{2,}'