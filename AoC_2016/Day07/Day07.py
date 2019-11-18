'''
--- Day 7: Internet Protocol Version 7 ---
While snooping around the local network of EBHQ, you compile a list of IP 
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like 
to figure out which IPs support TLS (transport-layer snooping).
An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or 
ABBA. An ABBA is any four-character sequence which consists of a pair of 
two different characters followed by the reverse of that pair, such as xyyx 
or abba. However, the IP also must not have an ABBA within any hypernet sequences, 
which are contained by square brackets.
'''
import unittest
import re
class TestGetSolution(unittest.TestCase):
    def test_checkTLS_solution1(self):
        self.assertEqual(checkTLS('abba[mnop]qrst'), True, "")
    def test_checkTLS_solution2(self):
        self.assertEqual(checkTLS('abcd[bddb]xyyx'), False, "")
    def test_checkTLS_solution3(self):
        self.assertEqual(checkTLS('aaaa[qwer]tyui'), False, "")
    def test_checkTLS_solution4(self):
        self.assertEqual(checkTLS('ioxxoj[asdfgh]zxcvbn'), True, "")
    def test_checkTLS_solution5(self):
        self.assertEqual(checkTLS('cvbn[as[dfgh]zx]ioxxoj'), True, "")
    def test_checkTLS_solution6(self):
        self.assertEqual(checkTLS('cvbn[asfff]dfghioxxoj[zxsad]asdafas'), True, "")

def checkTLS(ipv7address):
    retVal=False
    inBlock = False
    thisMachine=machine()
    for char in ipv7address:
        if thisMachine.state==0:
            if char == '[':
                inBlock=True                
                thisMachine.gotoStateZero()
            elif inBlock and char == ']':
                inBlock=False
                thisMachine.gotoStateZero()
            else:
                thisMachine.state=1
                thisMachine.first=char                
        elif thisMachine.state==1:
            if char == '[':
                inBlock=True                
                thisMachine.gotoStateZero()
            elif inBlock and char == ']':
                inBlock=False
                thisMachine.gotoStateZero()
            elif thisMachine.first==char:
                thisMachine.gotoStateZero()
            else:
                thisMachine.state=2
                thisMachine.second=char
        elif thisMachine.state==2:
            if char == '[':
                inBlock=True                
                thisMachine.gotoStateZero()
            elif inBlock and char == ']':
                inBlock=False
                thisMachine.gotoStateZero()
            elif thisMachine.second==char:
                thisMachine.state=3
            else:
                thisMachine.first=thisMachine.second
                thisMachine.second=char
        elif thisMachine.state==3:
            if char == '[':
                inBlock=True                
                thisMachine.gotoStateZero()
            elif inBlock and char == ']':
                inBlock=False
                thisMachine.gotoStateZero()
            elif thisMachine.first==char:
                if inBlock:
                    return False
                else:
                    retVal=True                    
                    thisMachine.gotoStateZero()
            else:
                thisMachine.first=thisMachine.second
                thisMachine.second=char
                thisMachine.state=2
    return retVal

class machine(object):
    def __init__(self):
        self.gotoStateZero()
    def gotoStateZero(self):
        self.state=0
        self.first=''
        self.second=''
if __name__ == '__main__':
    with open('Day07Data.txt','r')as inputFile:
        lines=inputFile.read().splitlines()
        print sum(map(checkTLS,lines))