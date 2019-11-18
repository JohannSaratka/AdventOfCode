'''
Created on 01.12.2017

--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

'''
import unittest
from collections import deque

class Test(unittest.TestCase):
    def testSpin(self):
        self.assertEqual(solve('s1',5), 'eabcd')
    def testExchange(self):
        self.assertEqual(solve('x3/4',5), 'abced')
    def testSwap(self):
        self.assertEqual(solve('pe/b',5), 'aecdb')
#     def testAvailableRegions(self):
#         self.assertEqual(solvePartTwo(65,8921), 309)

def solve(input_list, end = 16):
    start = 97
    prog_list = [chr(x) for x in xrange(start,start+end)]
    for command in input_list.split(','):
        if command[0] == 's':
            prog_list = rotate(prog_list,int(command[1:]))
        elif command[0] == 'x':
            src = int(command[1:command.index('/')])
            dst = int(command[command.index('/')+1:end])
            prog_list[src],prog_list[dst] = prog_list[dst],prog_list[src]
        elif command[0] == 'p':
            src = prog_list.index(command[1])
            dst = prog_list.index(command[3])
            prog_list[src],prog_list[dst] = prog_list[dst],prog_list[src]
    return ''.join(prog_list)

def rotate(l, n):
    return l[-n:] + l[:-n]   
 
def solvePartTwo(input_list, end = 16):
    start = 97
    prog_list = [chr(x) for x in xrange(start,start+end)]
    command_list = input_list.split(',')
    seen= list()
    reps=1000000000
    for i in xrange(reps):
        s = ''.join(prog_list)
        if s in seen:  # cycles are short; no runtime lost for comparing full list instead of s == seen[0]
            return seen[reps % i]
        seen.append(s)
        for command in command_list:
            if command[0] == 's':
                prog_list = rotate(prog_list,int(command[1:]))
            elif command[0] == 'x':
                src,dst = map(int,command[1:].split('/'))
                prog_list[src],prog_list[dst] = prog_list[dst],prog_list[src]
            elif command[0] == 'p':
                src = prog_list.index(command[1])
                dst = prog_list.index(command[3])
                prog_list[src],prog_list[dst] = prog_list[dst],prog_list[src]
        
    return ''.join(prog_list)

enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:            
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput)
            print solvePartTwo(puzzleInput)