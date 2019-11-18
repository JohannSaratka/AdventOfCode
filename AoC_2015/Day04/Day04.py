'''
Created on 03.12.2015

@author: Johann
'''
import unittest
from hashlib import md5

class Test(unittest.TestCase):
    def test_One(self):
        self.assertEqual(produceFiveZerosHash('abcdef'), 609043)
    def test_Two(self):
        self.assertEqual(produceFiveZerosHash('pqrstuv'), 1048970)    
        
def produceFiveZerosHash(key):
    m=md5()
    test="12345"
    num=1
    while(True):
        m=md5()
        m.update(key)
        m.update(str(num))
        test=m.hexdigest()
        if test[0:5]=='00000': break
        num+=1
    return num

def produceSixZerosHash(key):
    m=md5()
    test="123456"
    num=1
    while(True):
        m=md5()
        m.update(key)
        m.update(str(num))
        test=m.hexdigest()
        if test[0:6]=='000000': break
        num+=1
    return num

if __name__ == "__main__":
    #unittest.main()
    print produceFiveZerosHash('yzbqklnj')
    print produceSixZerosHash('yzbqklnj')