'''
Created on 02.12.2015

@author: Johann
'''
import unittest

class TestFindFloor(unittest.TestCase):
    def test_getFloor_isZero(self):
        self.assertEqual(getFloor('(())'), 0, "")
        self.assertEqual(getFloor('()()'), 0, "")
        
    def test_getFloor_isThree(self):
        self.assertEqual(getFloor('((('), 3, "")
        self.assertEqual(getFloor('))((((('), 3, "")
        
    def test_getFloor_isMinusOne(self):
        self.assertEqual(getFloor('())'), -1, "")
        self.assertEqual(getFloor('))('), -1, "")
    
    def test_getFloor_isMinusThree(self):
        self.assertEqual(getFloor(')))'), -3, "")
        self.assertEqual(getFloor(')())())'), -3, "")
    
    def test_enterBasementAt_PositionOne(self):
        self.assertEqual(enterBasementAt(')'), 1, "")
    
    def test_enterBasementAt_PositionFive(self):
        self.assertEqual(enterBasementAt('()())'), 5, "")
        
def getFloor(instructions):
    return sum([1 if x=='(' else -1 for x in instructions])

def enterBasementAt(instructions):
    s=0
    for num,x in enumerate(instructions):
        s=s+1 if x=='('else s-1
        if s<0 :
            return num+1
    return 0
   
if __name__ == '__main__':    
    #unittest.main()
    with open('Day01Data.txt','r')as name:
        for s in name:            
            print getFloor(s)
            print enterBasementAt(s)