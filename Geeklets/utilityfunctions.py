""" UTILITY FUNCTIONS
 ROBERT WOLTERMAN (xtacocorex) - 2012

 UTILITY FUNCTIONS REQUIRED FOR THE ULTIMATE WEATHER SCRIPT
"""

# CHANGELOG
# 21 APRIL 2012
#  - EXTRACTION FROM THE MAIN SCRIPT AND PUT INTO THE SERVICES MODULE

# MODULE IMPORTS
import urllib
from globals import *

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def myencode(instr):
    """
        myencode()
         - GETS THE LOCATION DATA
         - INPUT:  instr - INPUT STRING TO ENCODE PROPERLY FOR A URL
         - OUPUTS: rstr  - OUTPUT STRING OF PROPERLY ENCODED URL PORTION
    """
    rstr = instr
    rstr = rstr.replace(' ',SPACE)
    rstr = rstr.replace('=',EQUAL)
    rstr = rstr.replace('"',QUOTE)
    rstr = rstr.replace(':',SEMICOLON)
    rstr = rstr.replace('/',SLASH)
    rstr = rstr.replace('+',PLUS)
    rstr = rstr.replace('?',QUESTION)
    rstr = rstr.replace('&',AMPERSAND)
    rstr = rstr.replace('[',RBRACKET)
    rstr = rstr.replace(']',LBRACKET)
    rstr = rstr.replace('@',AT)
    rstr = rstr.replace('|',PIPE)
    # RETURN OUR ENCODED STRING
    return rstr

def printTable(matrix,size,justify="left"):
    # GET THE BIGGEST ELEMENT IN THE LIST
    big = 0
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            tmp = len(matrix[i][j])
            if tmp > big:
                big = tmp
    # ADD 2 TO BIG JUST TO SPACE THE TABLE PROPERLY
    big += 2
    # CREATE THE FORMAT
    fmt = "%s" * size[1]
    # JUSTIFY THE DATA IN THE LIST
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            tmp = matrix[i][j]
            if justify == 'left':
                matrix[i][j] = tmp.ljust(big)
            elif justify == 'right':
                matrix[i][j] = tmp.rjust(big)
            elif justify == 'center':
                matrix[i][j] = tmp.center(big)
    # PRINT THE DATA
    for i in xrange(size[0]):
        print fmt % tuple(matrix[i])

def getImage(loc,fname,path):
    """
        getImage()
         - DOWNLOADS AN IMAGE FROM THE INTERNET AND SAVES
           AS THE FILENAME PROVIDED AND IN THE PATH YOU PROVIDED
         - INPUT:  loc   - URL LOCATION OF IMAGE
                   fname - FILENAME OF THE SAVED FILE
                   path  - DIRECTORY STRUCTURE OF WHERE IMAGES SHOULD GO
         - OUPUTS: NONE
    """
    # GET THE DATA FROM THE INTERNET AND SAVE
    tmp = path + "/" + fname
    urllib.urlretrieve(loc,tmp)
    urllib.urlcleanup()
