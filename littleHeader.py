keepGoing = 1
juh = ''
while keepGoing:
  if juh == '':
      juh = input("what stringe 2 writh?\n")
  fillChar = '≡'
  smallChar = '~'
  outLen = 79

  fillLen = int((outLen - len(juh) - 2)/2)

  outStr1 = fillChar * fillLen + ' ' + juh + ' ' + fillChar * fillLen
  outStr2 = fillChar * (fillLen - 1) + ' /' + juh + ' ' + fillChar * fillLen

  print(outStr1 + '\n' + outStr2)
  print('\n')

  tildes = '~' * (76 - len(juh))
  print('# ' + tildes + ' ' + juh)
  
  juh = input("Enter another string to continue, or press enter to quit.\n")
  if juh == '':
    keepGoing = 0
  #end if k1.lower() == 'n'
# end while keepGoing