'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

import unittest


class Test(unittest.TestCase):
    testinput = ("initial state: #..#.#..##......###...###\n"
                    "\n"
                    "...## => #\n"
                    "..#.. => #\n"
                    ".#... => #\n"
                    ".#.#. => #\n"
                    ".#.## => #\n"
                    ".##.. => #\n"
                    ".#### => #\n"
                    "#.#.# => #\n"
                    "#.### => #\n"
                    "##.#. => #\n"
                    "##.## => #\n"
                    "###.. => #\n"
                    "###.# => #\n"
                    "####. => #\n")
    def testLicenseFile(self):   
        self.assertEqual(solve(self.testinput.splitlines()), 325)
        
    def testSecondStrategy(self):   
        self.assertEqual(solvePartTwo(self.testinput), 66)

def solve(plants_instructions, generations=20):    
    init_state=plants_instructions[0][15:]
    rules=plants_instructions[2:]
    rules_dict = {rule[:5]:rule[9] for rule in rules}
    left=0
    for g in range(generations):        
        next_state=""
        init_state='...'+init_state+'...'
        for i in range(0,len(init_state)-4):
            pot = init_state[i:i+5]
            try:
                next_pot = rules_dict[pot]
            except KeyError:
                next_pot='.'
            if i==0 and next_pot=='#':
                left += 1
            next_state += next_pot
        init_state=next_state
    
    has_plant=[i-20 for i,pot in enumerate(init_state) if pot=='#']
    return sum(has_plant)

def solvePartTwo(license_file):
    pass

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput.splitlines()))
        print(solvePartTwo(puzzleInput))

    