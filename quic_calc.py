'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

[description]

1--------10--------20--------30--------40--------50--------60--------70--------
'''

def dooth(nh,nl):
  sin2c = (nh**2-nl**2)/(nh**2)
  d_lam = 3/2 * nh/((nh**2-nl**2)**0.5)
  print("sin2c = " + str(sin2c))
  print("d/λ = " + str(d_lam))
  return (sin2c,d_lam)
#end def dooth(nh,nl)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  LN = 2.2080180
  LN_eff = 1.953929
  box = 1.44575
  (s,dL) = dooth(LN,box)
  (s_1,dL_1) = dooth(LN_eff,box)
# end if __name__ == "__main__"