'''
Created on 01.12.2017

--- Day 14: Disk Defragmentation ---

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

--- Part Two ---
Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?
'''
import unittest
from AoC_2017.Day10.solution import KnotHash
import pickle

class Test(unittest.TestCase):
    @unittest.skip('Currently not necessary')
    def testUsedSquares(self):
        self.assertEqual(solve('flqrgnkx'), 8108)
        
    def testAvailableRegions(self):
        with open("testdata.pickle","rb") as f:
            data = pickle.load(f)
        ccl = ConnectedComponentLabeling(data)
        ccl.twoPass()
        self.assertEqual(ccl.getNumOfRegions(), 1242)

def solve(key_string):
    used_squares = 0
    for i in xrange(128):
        kh = KnotHash(256,key_string+'-'+str(i))
        kh.generateHash()
        bin_hash = kh.getBinaryHash()
        used_squares+=bin_hash.count('1')
    return used_squares
    

def solvePartTwo(key_string):
    data=[]
    for i in xrange(128):
        kh = KnotHash(256,key_string+'-'+str(i))
        kh.generateHash()
        bin_hash = kh.getBinaryHash()
        data.append(map(int,bin_hash))
    ccl = ConnectedComponentLabeling(data)
    ccl.twoPass()
    return ccl.getNumOfRegions()
    
class ConnectedComponentLabeling(object):
    def __init__(self,data):
        self.data = data
        self.linked = dict()
        self.dim_x = len(data[0])
        self.dim_y = len(data)
        self.labels = [[0 for _ in xrange(self.dim_x)] for _ in xrange(self.dim_y)]#structure with dimensions of data, initialized with the value of Background
        self.next_label = 1
        self.background = 0
        
        
    def twoPass(self):
        ''' see https://en.wikipedia.org/wiki/Connected-component_labeling'''        
        #First pass    
        for row in xrange(self.dim_x):
            for column in xrange(self.dim_y):
                if self.data[row][column] is not self.background:
                    neighbors = self.getNeighbors(self.data,row,column)#connected elements with the current element's value
            
                    if not neighbors:
                        self.linked[self.next_label] = set([self.next_label])#set containing NextLabel
                        self.labels[row][column] = self.next_label
                        self.next_label += 1
            
                    else:            
                        #Find the smallest label
                        L = set.union(*[self.linked[self.labels[n_x][n_y]] for n_x,n_y in neighbors]) # get all links from neighbors labels
                        self.labels[row][column] = min(L)
                        for label in L:
                            self.linked[label] = self.linked[label] | set(L)
    
        #Second pass
        for row in xrange(self.dim_x):
            for column in xrange(self.dim_y):
                if self.data[row][column] is not self.background:
                    self.labels[row][column] = self.getLowestConnectedLabel(self.labels[row][column])

    def getNeighbors(self,data,x,y):
        # returns all connected elements with the current element's value
        # only look west and north
        neighbors = list()        
        if (x-1 >= 0) and data[x-1][y]==data[x][y]:
            neighbors.append([x-1,y])
#         if (x+1 < self.dim_x) and data[x+1][y]==data[x][y]:
#             neighbors.append([x+1,y])
        if (y-1 >= 0) and data[x][y-1]==data[x][y]:
            neighbors.append([x,y-1])
#         if (y+1 < self.dim_y) and data[x][y+1]==data[x][y]:
#             neighbors.append([x,y+1])    
        return neighbors
    
    def getLowestConnectedLabel(self,value):
        return min(self.linked[value])
    
    def getNumOfRegions(self):
        return (len(set().union(*self.labels))-1)

enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()        
            print solve(puzzleInput)
            print solvePartTwo(puzzleInput)