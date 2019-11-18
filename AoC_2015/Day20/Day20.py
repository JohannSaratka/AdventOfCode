'''
Created on 03.12.2015

@author: Johann
'''
import unittest
from math import sqrt

class Test(unittest.TestCase):
    def test_getLowestHouse_secondHouse(self):
        self.assertEqual(getLowestHouse(30), 2)
    def test_getLowestHouse_thirdHouse(self):
        self.assertEqual(getLowestHouse(40), 3)
    def test_getLowestHouse_fourthHouse(self):
        self.assertEqual(getLowestHouse(70), 4)
    def test_getLowestHouse_fifthHouse(self):
        self.assertEqual(getLowestHouse(60), 5)
    def test_getLowestHouse_sixthHouse(self):
        self.assertEqual(getLowestHouse(120), 6)
    def test_getLowestHouse_seventhHouse(self):
        self.assertEqual(getLowestHouse(80), 7)
    def test_getLowestHouse_eigthHouse(self):
        self.assertEqual(getLowestHouse(150), 8)
    def test_getLowestHouse_ninethHouse(self):
        self.assertEqual(getLowestHouse(130), 9)

##############################################################
### cartesian product of lists ##################################
##############################################################

def appendEs2Sequences(sequences,es):
    result=[]
    if not sequences:
        for e in es:
            result.append([e])
    else:
        for e in es:
            result+=[seq+[e] for seq in sequences]
    return result


def cartesianproduct(lists):
    """
    given a list of lists,
    returns all the possible combinations taking one element from each list
    The list does not have to be of equal length
    """
    return reduce(appendEs2Sequences,lists,[])

##############################################################
### prime factors of a natural ##################################
##############################################################

def primefactors(n):
    '''lists prime factors, from greatest to smallest'''  
    i = 2
    while i<=sqrt(n):
        if n%i==0:
            l = primefactors(n/i)
            l.append(i)
            return l
        i+=1
    return [n]      # n is prime


##############################################################
### factorization of a natural ##################################
##############################################################

def factorGenerator(n):
    p = primefactors(n)
    factors={}
    for p1 in p:
        try:
            factors[p1]+=1
        except KeyError:
            factors[p1]=1
    return factors

def divisors(n):
    factors = factorGenerator(n)
    divisors=[]
    listexponents=[map(lambda x:k**x,range(0,factors[k]+1)) for k in factors.keys()]
    listfactors=cartesianproduct(listexponents)
    for f in listfactors:
        divisors.append(reduce(lambda x, y: x*y, f, 1))
    divisors.sort()
    return divisors

def getLowestHouse(presents):
    n=10000
    testsum=n
    # this will not work with the unit tests but is the correct answer to the actual puzzle
    while(testsum<(presents/10)):
        n+=1
        print n
        testDivisors=list(divisors(n))
        testsum=sum(testDivisors) if len(testDivisors)>1 else testDivisors[0]        
    return n
            
if __name__ == "__main__":
    #unittest.main()
    numPresents=34000000
    print getLowestHouse(numPresents)
        