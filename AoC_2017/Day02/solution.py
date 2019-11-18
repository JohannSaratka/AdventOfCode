'''
Created on 01.12.2017

--- Day 2: Corruption Checksum ---

Part One
The spreadsheet consists of rows of apparently-random numbers. To make sure the recovery 
process is on the right track, they need you to calculate the spreadsheet's checksum. 
For each row, determine the difference between the largest value and the smallest value; 
the checksum is the sum of all of these differences.

For example, given the following spreadsheet:

5 1 9 5
7 5 3
2 4 6 8

    The first row's largest and smallest values are 9 and 1, and their difference is 8.
    The second row's largest and smallest values are 7 and 3, and their difference is 4.
    The third row's difference is 6.

In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.

Part Two
It sounds like the goal is to find the only two numbers in each row where one evenly divides the other - that is, where the result of the division operation is a whole number. They would like you to find those numbers on each line, divide them, and add up each line's result.

For example, given the following spreadsheet:

5 9 2 8
9 4 7 3
3 8 6 5

    In the first row, the only two numbers that evenly divide are 8 and 2; the result of this division is 4.
    In the second row, the two numbers are 9 and 3; the result is 3.
    In the third row, the result is 2.

In this example, the sum of the results would be 4 + 3 + 2 = 9.
'''
import unittest


class Test(unittest.TestCase):
    def testChecksum(self):
        self.assertEqual(solve('5 1 9 5\n7 5 3\n2 4 6 8'), 18)
    def testEvenlyDivisable(self):
        self.assertEqual(solvePartTwo('5 9 2 8\n9 4 7 3\n3 8 6 5'), 9)    

def solve(inputList):
    sumTotal = 0
    for line in inputList.split('\n'):
        values = map(int,line.split())
        sumTotal += max(values) - min(values)

    return sumTotal

def solvePartTwo(inputList):
    sumTotal = 0
    for line in inputList.split('\n'):
        values = sorted(map(int,line.split()))
        possibleDivisions = list()
        for y in range(len(values)):
            possibleDivisions.extend([divmod(x,values[y]) for x in values[y:]])
        divisor = filter(lambda z:(z[1] == 0) and (z[0] != 1),possibleDivisions)[0]
        sumTotal += divisor[0]
    return sumTotal

enableUnitTest = False
if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput),                
            print solvePartTwo(puzzleInput)
    