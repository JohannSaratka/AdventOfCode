'''
Created on 01.12.2017

--- Day 10: Knot Hash ---
This hash function simulates tying a knot in a circle of string with 256 marks on it. Based on the input to be hashed, the function repeatedly selects a span of string, brings the ends together, and gives the span a half-twist to reverse the order of the marks within it. After doing this many times, the order of the marks is used to build the resulting hash.

  4--5   pinch   4  5           4   1
 /    \  5,0,1  / \/ \  twist  / \ / \
3      0  -->  3      0  -->  3   X   0
 \    /         \ /\ /         \ / \ /
  2--1           2  1           2   5

To achieve this, begin with a list of numbers from 0 to 255, a current position which begins at 0 (the first element in the list), a skip size (which starts at 0), and a sequence of lengths (your puzzle input). Then, for each length:

    Reverse the order of that length of elements in the list, starting with the element at the current position.
    Move the current position forward by that length plus the skip size.
    Increase the skip size by one.

The list is circular; if the current position and the length try to reverse elements beyond the end of the list, the operation reverses using as many extra elements as it needs from the front of the list. If the current position moves past the end of the list, it wraps around to the front. Lengths larger than the size of the list are invalid.

Here's an example using a smaller list:

Suppose we instead only had a circular list containing five elements, 0, 1, 2, 3, 4, and were given input lengths of 3, 4, 1, 5.

    The list begins as [0] 1 2 3 4 (where square brackets indicate the current position).
    The first length, 3, selects ([0] 1 2) 3 4 (where parentheses indicate the sublist to be reversed).
    After reversing that section (0 1 2 into 2 1 0), we get ([2] 1 0) 3 4.
    Then, the current position moves forward by the length, 3, plus the skip size, 0: 2 1 0 [3] 4. Finally, the skip size increases to 1.

    The second length, 4, selects a section which wraps: 2 1) 0 ([3] 4.
    The sublist 3 4 2 1 is reversed to form 1 2 4 3: 4 3) 0 ([1] 2.
    The current position moves forward by the length plus the skip size, a total of 5, causing it not to move because it wraps around: 4 3 0 [1] 2. The skip size increases to 2.

    The third length, 1, selects a sublist of a single element, and so reversing it has no effect.
    The current position moves forward by the length (1) plus the skip size (2): 4 [3] 0 1 2. The skip size increases to 3.

    The fourth length, 5, selects every element starting with the second: 4) ([3] 0 1 2. Reversing this sublist (3 0 1 2 4 into 4 2 1 0 3) produces: 3) ([4] 2 1 0.
    Finally, the current position moves forward by 8: 3 4 2 1 [0]. The skip size increases to 4.

In this example, the first two numbers in the list end up being 3 and 4; to check the process, you can multiply them together to produce 12.

However, you should instead use the standard list size of 256 (with values 0 to 255) and the sequence of lengths in your puzzle input. Once this process is complete, what is the result of multiplying the first two numbers in the list?
'''
import unittest


class Test(unittest.TestCase):

    def testGroups(self):
        nums=solve(5,'3,4,1,5')
        self.assertEqual(nums[0]*nums[1], 12)
        
    def testFullHash(self):
        test_data = [['','a2582a3a0e66e6e86e3812dcb672a272'],
                     ['AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'],
                     ['1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'],
                     ['1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e'],
                     ]
        for data, expectation in test_data:
            actual = solvePartTwo(data)
            self.assertEqual(actual, expectation,"Data: " + data + "\nExpected: " + str(expectation)+"\nActual: " + str(actual))

class KnotHash(object):
    def __init__(self,size,inp_string):
        self.size = size
        self.seq_of_lengths = self.getSequenceOfLengths(inp_string)
        self.numbers = range(size)
        self.current_pos = 0
        self.skip_size = 0
        
    def getSequenceOfLengths(self,inp_string):
        seq = map(ord,inp_string)
        seq.extend([17, 31, 73, 47, 23])
        return seq
    
    def runHashRound(self):
        for length in self.seq_of_lengths:        
            select =[ self.numbers[i % self.size] for i in xrange(self.current_pos,self.current_pos + length)]
            select.reverse()
            for n,val in enumerate(select):
                self.numbers[(self.current_pos + n) % self.size] = val
            self.current_pos += (length + self.skip_size) 
            self.current_pos %= self.size
            self.skip_size += 1
            self.skip_size %= self.size
            
    def generateHash(self):
        for _ in xrange(64):
            self.runHashRound()
        self.dense_hash = self.compressHash(16)
        self.hash_string = ''.join('{:02x}'.format(x) for x in self.dense_hash)
        
    def compressHash(self,block_length):
        output = []
        for value_list in [self.numbers[i:i+block_length] for i in xrange(0,self.size,block_length)]:
            output.append(reduce(lambda a, b: a ^ b,value_list))
        return output
    def getBinaryHash(self):
        return ''.join('{:08b}'.format(x) for x in self.dense_hash)
def solve(size,input_string):
    kh = KnotHash(size,input_string)
    kh.seq_of_lengths = map(int,input_string.split(','))
    kh.runHashRound()
    return kh.numbers

def solvePartTwo(input_string):
    kh = KnotHash(256,input_string)
    kh.generateHash()
    return kh.hash_string
                
            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            nums = solve(256,puzzleInput)            
            print nums[0]*nums[1]
            print solvePartTwo(puzzleInput)
    