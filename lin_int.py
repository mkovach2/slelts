# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>
# Modified: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Sphinx docstring for functions:
# """[Summary]

# :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
# :type [ParamName]: [ParamType](, optional)
# ...
# :raises [ErrorType]: [ErrorDescription]
# ...
# :return: [ReturnDescription]
# :rtype: [ReturnType]
# """

def linInterp(a0,a1,b0,b1):
    m_a = (a1[1] - a0[1])/(a1[0] - a0[0])
    m_b = (b1[1] - b0[1])/(b1[0] - b0[0])
    
    x_out = (b0[1] - a0[1] + m_a * a0[0] - m_b * b0[0])/(m_a - m_b)
    y_out = m_a * (x_out - a0[0]) + a0[1]
    
    return(x_out, y_out)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    
    print(linInterp(
        a0 = (),
        a1 = (),
        b0 = (),
        b1 = (),
    ))
    
    
    
    
    
#end if __name__ == "__main__"
