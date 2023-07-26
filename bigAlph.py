from copy import deepcopy
import bigAlph_letters as bal

bigChar = bal.bigChar()
bigChar_double = bal.bigChar_double()


wincmd = 1 # a bool to set if you plan to run this from the windows
# command line
if 0:
    nChar = "─"
    pChar = "█"
# end if 1
else:
    nChar = "░"  # default '─'
    pChar = "█"  # default '█'
# end else

if wincmd:
    inStr = input("enter word to enalrge (use \\n for newline):\t")
    comChar = input("enter comment character (press enter to skip):\t")
    instr_list = inStr.split("\\n")
else:
    inStr = "test: aAbBcC!@#$%\n&123"
    comChar = ""
    instr_list = inStr.split("\n")

stillGoing = 1
giveKeyMsg = 0  # error flag
print_py_str = 1
spyder_bookmark = 1 # adds a spyder-style code bookmark
bookmark_str = '#----'

while stillGoing:
    outstr_list = []
    
    for st_in in instr_list:
        outD = deepcopy(bigChar[st_in[0]])
        for q in range(1, len(st_in)):
            try:
                d2 = st_in[q]
                outD[0] = outD[0] + bigChar[d2][0]
                outD[1] = outD[1] + bigChar[d2][1]
                outD[2] = outD[2] + bigChar[d2][2]
                outD[3] = outD[3] + bigChar[d2][3]
                outD[4] = outD[4] + bigChar[d2][4]
            except KeyError:
                giveKeyMsg = 1
                problemKey = st_in[q]
                break
        
        if giveKeyMsg:
            print('key not in dict:\t"' + problemKey + '"')
        
        outstr_list.append(outD)
        
        
        
    if print_py_str:
        print("\nas python strings:")
        
        eol = "\\n\" +\\"
        
        print("double width:")
        for out_d in outstr_list:
            for r in range(0, 5):
                print(comChar + "\"" + (out_d[r].replace("─", 2 * nChar)).replace("█", 2 * pChar) + eol)
            if len(outstr_list) > 1:
                print("\"" + nChar * 2 * len(out_d[r]) + eol)
                
        print('\n')
        for out_d in outstr_list:
            for r in range(0, 5):
                print(comChar + "\"" + out_d[r].replace("─", nChar).replace("█", pChar) + eol)
            if len(outstr_list) > 1:
                print("\"" + nChar * len(out_d[r]) + eol)
        
    print("\ndouble width:")
    for out_d in outstr_list:
        for r in range(0, 5):
            print(comChar + (out_d[r].replace("─", 2 * nChar)).replace("█", 2 * pChar))
        if len(outstr_list) > 1:
            print(nChar * 2 * len(out_d[r]))
    if spyder_bookmark:
        print(bookmark_str + ' ' + inStr)
            
    print('\n')
    for out_d in outstr_list:
        for r in range(0, 5):
            print(comChar + out_d[r].replace("─", nChar).replace("█", pChar))
        if len(outstr_list) > 1:
            print(nChar * len(out_d[r]))
    if spyder_bookmark:
        print(bookmark_str + ' ' + inStr)


    inStr = input("\nEnter another string to continue, or press enter to quit.\n")
    if inStr == '':
        stillGoing = 0
    else:
        if wincmd:
            comChar = input("enter comment character (press enter to skip):\t")
            instr_list = inStr.split("\\n")
        else:
            comChar = ""
            instr_list = inStr.split("\n")

if wincmd:
    input("finished.  press enter to close.\n")
else:
    print("finished.")
