'''
Created on 29.11.2017

@author: johann
'''
import unittest


class Test(unittest.TestCase):
    def testSignal(self):
        Signal('123','x')
        self.assertEqual(123, allWiresDict['x'])
        
    def testNotSignal(self):
        NotSignal('123','h')
        self.assertEqual(65412, allWiresDict['h'])
        
    def testPropagationOnce(self):
        propagateSignal()
        
allWiresDict = dict()

class Signal(object):
    def __init__(self,inputWire,outputWire):
        self.inputWire = inputWire
        self.outputWire = outputWire
        self.setValue()
        
    def setValue(self):
        if self.inputWire.isdigit():
            allWiresDict[self.outputWire] = int(self.inputWire)
        else:
            allWiresDict[self.outputWire] = self

class NotSignal(Signal):
    def setValue(self):
        if self.inputWire.isdigit():
            allWiresDict[self.outputWire] = ~int(self.inputWire) & 0xFFFF 
        else:
            allWiresDict[self.outputWire] = self

def propagateSignal():
    wiresWithValue = {x:allWiresDict[x] for x in allWiresDict.keys() if type(allWiresDict[x]) == int }
    for wire,value in wiresWithValue:
        print wire,value
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()