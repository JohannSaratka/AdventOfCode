'''
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?


'''

import unittest
import re

class Test(unittest.TestCase):
    def testExampleIsValid(self):
        self.assertEqual(checkCriteria('122345'),True)
    
    def testDigitsAllTheSameIsValid(self):
        self.assertEqual(checkCriteria('111111'),True)
        
    def testDecreasingDigitsIsInvalid(self):
        self.assertEqual(checkCriteria('223450'),False)
        
    def testNoDoubleDigitsIsInvalid(self):
        self.assertEqual(checkCriteria('123789'),False)
    
    def testExampleIsValidPart2(self):
        self.assertEqual(checkCriteriaPart2('122345'),True)
    
    def testDigitsAllTheSameIsInvalidPart2(self):
        self.assertEqual(checkCriteriaPart2('111111'),False)
        
    def testDecreasingDigitsIsInvalidPart2(self):
        self.assertEqual(checkCriteriaPart2('223450'),False)
        
    def testNoDoubleDigitsIsInvalidPart2(self):
        self.assertEqual(checkCriteriaPart2('123789'),False)
        
    def testMultipleDoubleDigitsIsValidPart2(self):
        self.assertEqual(checkCriteriaPart2('112233'),True)
        
    def testLargerGroupIsInvalidPart2(self):
        self.assertEqual(checkCriteriaPart2('223444'),False)
        
    def testLargerGroupWithDoubleIsValidPart2(self):
        self.assertEqual(checkCriteriaPart2('111122'),True)

digits_incrementing = re.compile(r"""^(?=0*1*2*3*4*5*6*7*8*9*$)# positive lookahead digits only incrementing
                                """,re.VERBOSE)
digits_twice = re.compile(r""".*(\d)\1 # capture digit and match if repeated
                        """,re.VERBOSE)
def checkCriteria(digits):
    return (
            (digits_twice.match(digits) is not None) and 
            (digits_incrementing.match(digits) is not None)
        )

def checkCriteriaPart2(digits):
    if checkCriteria(digits):
        paired = list(map(list, zip(digits, digits[1:]))) 
                
    return False

    
def solve(password_range):
    start, end = map(int, password_range[0].split('-'))
    count = 0
    for password in range(start,end+1):
        digits = str(password)
        
        count += 1 if checkCriteria(digits) else 0
        
    return count

def solvePartTwo(password_range):
    start, end = map(int, password_range[0].split('-'))
    count = 0
    for password in range(start,end+1):
        digits = str(password)
        count += 1 if checkCriteriaPart2(digits) else 0
         
    return count

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solvePartTwo(puzzleInput)))

    