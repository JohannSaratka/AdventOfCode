'''
Created on 03.12.2015

@author: Johann
'''
import unittest
import re

class Test(unittest.TestCase):
    def test_readCircuit(self):
        pass
    
class GateNode(object):
    def __init__(self,in1,in2,out):
        self.in1=in1
        self.in2=in2
        self.out=out
        
class ANDNode(GateNode):
    def setOutWire(self):
        self.out.value=self.in1&self.in2
        
class ORNode(GateNode):
    def setOutWire(self):
        self.out.value=self.in1>>self.in2
        
class LSHIFTNode(GateNode):
    def setOutWire(self):
        self.out.value=self.in1<<self.in2
        
class RSHIFTNode(GateNode):
    def setOutWire(self):
        self.out.value=self.in1&self.in2
        
class NOTNode(GateNode):
    def setOutWire(self):
        self.out.value=not self.in1
        
class Wire(object):
    def __init__(self,value=None):
        self.value=value
    
emulatedWire={}

if __name__ == "__main__":
    #unittest.main()
    with open('Day07Data.txt','r')as name:
        aIsNumber=False
        for line in name:
            source,wire=line.strip('\n').split(" -> ")
            if source.isdigit():
                emulatedWire[wire]=Wire(int(source))
            else:
                test=source.split()
                
        
            