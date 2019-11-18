'''
Created on 02.12.2017

--- Day 2: Inventory Management System ---

Part One
To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number that have an ID containing exactly two of any letter and then separately counting those with exactly three of any letter. You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

For example, if you see the following box IDs:

    abcdef contains no letters that appear exactly two or three times.
    bababc contains two a and three b, so it counts for both.
    abbcde contains two b, but no letter appears exactly three times.
    abcccd contains three c, but no letter appears exactly two times.
    aabcdd contains two a and two d, but it only counts once.
    abcdee contains two e.
    ababab contains three a and three b, but it only counts once.

Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?

'''

import unittest
from collections import Counter
import difflib
from difflib import get_close_matches

class Test(unittest.TestCase):
    def testZeroLettersTwoTimesZeroLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('abcdef'), (0,0))
        
    def testOneLettersTwoTimesOneLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('bababc'), (1,1))
        
    def testOneLettersTwoTimesZeroLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('abbcde'), (1,0))
        
    def testZeroLettersTwoTimesOneLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('abcccd'), (0,1))
        
    def testTwoLettersTwoTimesZeroLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('aabcdd'), (1,0))
        
    def testZeroLettersTwoTimesTwoLettersThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('ababab'), (0,1))
         
    def testLettersMoreThanThreeTimes(self):
        self.assertEqual(countLettersExactlyTwoAndThreeTimes('abbbcb'), (0,0))

    def testChechsumIsCorrect(self):
        self.assertEqual(solve('abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab\n'), 12)
        
    def testDifferByOneCharacter(self):
        self.assertEqual(solvePartTwo('abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz'), 'fgij')
            
def countLettersExactlyTwoAndThreeTimes(letters):
    cnt = Counter(letters)
    return (int(any([l == 2 for l in cnt.values()])),int(any([l == 3 for l in cnt.values()])))
    

def solve(list_of_IDs):
    two = 0
    three = 0
    for ident in list_of_IDs.split('\n'):
        letter_two_times, letter_three_times = countLettersExactlyTwoAndThreeTimes(ident)
        two += letter_two_times
        three += letter_three_times        
    return two*three

def solvePartTwo(list_of_IDs):
    list_of_IDs = list_of_IDs.split('\n')
    # ensure the IDs differ in exactly one char
    cutoff_percent = round((len(list_of_IDs[0])-1)/len(list_of_IDs[0]),2)
    for ident in list_of_IDs:
        diff = get_close_matches(ident, list_of_IDs, cutoff = cutoff_percent)
        if len(diff)>1:
            return ''.join([i for i,j in zip(diff[0],diff[1]) if i==j])

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput))
        print(solvePartTwo(puzzleInput))

    