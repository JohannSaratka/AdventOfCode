'''
--- Day 3: Squares With Three Sides ---
Now that you can think clearly, you move deeper into the labyrinth of 
hallways and office furniture that makes up this part of Easter Bunny HQ. 
This must be a graphic design department; the walls are covered in 
specifications for triangles.
Or are they?
The design document gives the side lengths of each triangle it describes, 
but... 5 10 25? Some of these aren't triangles. You can't help but mark 
the impossible ones.
In a valid triangle, the sum of any two sides must be larger than the 
remaining side. For example, the "triangle" given above is impossible, 
because 5 + 10 is not larger than 25.
In your puzzle input, how many of the listed triangles are possible?
'''
import unittest
from itertools import chain

class TestGetSolution(unittest.TestCase):
    def test_isValidTriangle_solution1(self):
        self.assertEqual(isValidTriangle('5 10 25'), False, "")

def isValidTriangle(lengths):
    a,b,c = map(int,lengths.split())
    return (a+b>c)and(a+c>b)and(b+c>a)
'''
--- Part Two ---
Now that you've helpfully marked up their design documents, it occurs to you that 
triangles are specified in groups of three vertically. Each set of three numbers in a 
column specifies a triangle. Rows are unrelated.
For example, given the following specification, numbers with the same hundreds digit 
would be part of the same triangle:
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles 
are possible?
'''
if __name__ == '__main__':
    with open('Day03Data.txt','r')as inputFile:
        #lines=inputFile.read().splitlines()
        #validTriangles=map(isValidTriangle,lines)
        #print sum(validTriangles)
        lines=[line.split() for line in inputFile]
        rowsFlat=list(chain.from_iterable(map(list, zip(*lines))))
        triangles=[rowsFlat[i:i + 3] for i in xrange(0, len(rowsFlat), 3)]
        validTriangles=map(isValidTriangle,[" ".join(triangle) for triangle in triangles])
        print sum(validTriangles)
        