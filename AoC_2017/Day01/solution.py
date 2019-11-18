'''
Created on 01.12.2017

--- Day 1: Inverse Captcha ---

Part One
The captcha requires you to review a sequence of digits (your puzzle input) and find the sum 
of all digits that match the next digit in the list. The list is circular, so the digit after 
the last digit is the first digit in the list.

For example:

    1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and 
    the third digit (2) matches the fourth digit.
    1111 produces 4 because each digit (all 1) matches the next.
    1234 produces 0 because no digit matches the next.
    91212129 produces 9 because the only digit that matches the next one is the last digit, 9.

Part Two
Now, instead of considering the next digit, it wants you to consider the digit halfway around 
the circular list. That is, if your list contains 10 items, only include a digit in your sum if 
the digit 10/2 = 5 steps forward matches it. Fortunately, your list has an even number of elements.

For example:

    1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
    1221 produces 0, because every comparison is between a 1 and a 2.
    123425 produces 4, because both 2s match each other, but no other digit has a match.
    123123 produces 12.
    12131415 produces 4.
'''

import unittest


class Test(unittest.TestCase):
    def testMatchTwice(self):
        self.assertEqual(solve('1122'), 3)
        
    def testMatchAll(self): 
        self.assertEqual(solve('1111'), 4)
    
    def testMatchNone(self):
        self.assertEqual(solve('1234'), 0)
        
    def testMatchLastAndFirst(self):
        self.assertEqual(solve('91212129'), 9)
        
    def testPartTwoMatchTwice(self):
        self.assertEqual(solvePartTwo('123425'), 4)
        
    def testPartTwoMatchAll(self): 
        self.assertEqual(solvePartTwo('1212'), 6)
    
    def testPartTwoMatchNone(self):
        self.assertEqual(solvePartTwo('1221'), 0)
        
    def testPartTwoMatchLastAndFirst(self):
        self.assertEqual(solvePartTwo('123123'), 12)
        
    def testPartTwoMatchOneTwoThree(self):
        self.assertEqual(solvePartTwo('12131415'), 4)
        
def solve(inputList):
    inputList += inputList[0]
    
    sumTotal = 0
    for i,digit in enumerate(inputList[:-1]):
        if digit == inputList[i + 1]:
            sumTotal += int(digit)
    return sumTotal

def solvePartTwo(inputList):
    halfway = len(inputList)/2
    inputList += inputList
    
    sumTotal = 0
    for i,digit in enumerate(inputList[:-(halfway*2)]):
        if digit == inputList[i + halfway]:
            sumTotal += int(digit)
    return sumTotal

enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            for line in inFile:
                print solve(line.rstrip()),                
                print solvePartTwo(line.rstrip())
    