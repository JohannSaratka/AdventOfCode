'''
Created on 03.12.2015

@author: Johann
'''
import unittest

class Test(unittest.TestCase):
    def test_getSizeDifference_NoChars(self):
        self.assertEquals(getSizeDifference(""), 2)
    def test_getSizeDifference_String(self):
        self.assertEquals(getSizeDifference("abc"), 2)
    def test_getSizeDifference_EscapeDoubleQuote(self):
        self.assertEquals(getSizeDifference("aaa\"aaa"), 3)
    def test_getSizeDifference_EscapeBackslash(self):
        self.assertEquals(getSizeDifference("aaa\\aaa"), 3)
    def test_getSizeDifference_EscapeAscii(self):
        self.assertEquals(getSizeDifference("\x27"), 5)

def getSizeDifference(strng):
    strng=strng.rstrip()
    sizeMemory=len(strng.replace('"',''))
    sizeCode=len(repr(strng))
    return sizeCode-sizeMemory

if __name__ == "__main__":
    unittest.main()
    with open('Day08Data.txt','r')as f:
        print sum(map(getSizeDifference,f))