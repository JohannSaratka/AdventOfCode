'''
Created on 02.12.2015

@author: Johann
'''
import unittest
from twisted.internet.test.test_endpoints import WrappingFactoryTests

class TestFindFloor(unittest.TestCase):
    def test_getWrapping_isCorrect(self):
        self.assertEqual(getWrapping('2x3x4'), 58, "")
        self.assertEqual(getWrapping('1x1x10'), 43, "")
    
    def test_getWrapping_differentOrdering(self):
        self.assertEqual(getWrapping('4x3x2'), 58, "")
        self.assertEqual(getWrapping('1x10x1'), 43, "")
    
    def test_getRibbon_isCorrect(self):
        self.assertEqual(getRibbon('2x3x4'), 34, "")
        self.assertEqual(getRibbon('1x1x10'), 14, "")
    
    def test_getRibbon_differentOrdering(self):
        self.assertEqual(getRibbon('4x3x2'), 34, "")
        self.assertEqual(getRibbon('1x10x1'), 14, "")

def getWrapping(dimensions):
    length,width,height=map(int,dimensions.split('x'))
    surface=2*length*width+2*width*height+2*height*length
    slack=min([length*width,width*height,height*length])
    return surface+slack

def getRibbon(dimensions):
    length,width,height=sorted(map(int,dimensions.split('x')))
    wrap=2*width+2*length
    bow=length*width*height
    return wrap+bow

if __name__ == '__main__':
    #unittest.main()
    wrapping=0
    ribbon=0
    with open('Day02Data.txt','r')as name:
        for line in name:
            wrapping+= getWrapping(line)
            ribbon+=getRibbon(line)
    print wrapping
    print ribbon