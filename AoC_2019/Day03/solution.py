'''
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest intersection?

--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

'''

import unittest
import sys

class Test(unittest.TestCase):
    def testWirePath1(self):
        self.assertEqual(solve(['R8,U5,L5,D3','U7,R6,D4,L4']),6)
        
    def testWirePath2(self):        
        self.assertEqual(solve(['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                                'U62,R66,U55,R34,D71,R55,D58,R83']),159)
        
    def testWirePath3(self):
        self.assertEqual(solve(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                                'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']),135)
        
    def testWirePath4(self):
        self.assertEqual(solvePartTwo(['R8,U5,L5,D3','U7,R6,D4,L4']),30)
        
    def testWirePath5(self):        
        self.assertEqual(solvePartTwo(['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                                'U62,R66,U55,R34,D71,R55,D58,R83']),610)
        
    def testWirePath6(self):
        self.assertEqual(solvePartTwo(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                                'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']),410)
        
class line():
    convert={'R':(1,0),'L':(-1,0),'U':(0,1),'D':(0,-1),}
    def __init__(self,pos,direction,length):
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = self.x1 + length * self.convert[direction][0]
        self.y2 = self.y1 + length * self.convert[direction][1]
        self.length = length
        self.direction = direction
        
        if self.x1 > self.x2:
            self.x1 , self.x2 = self.x2 , self.x1
        if self.y1 > self.y2:
            self.y1 , self.y2 = self.y2 , self.y1
            
        self.up_down = direction == 'U' or direction == 'D'
        
    def __repr__(self):
        return '1: ({s.x1}, {s.y1}), 2: ({s.x2}, {s.y2})'.format(s=self)
    
    def getHead(self):
        if(self.direction == 'R' or self.direction == 'U'):
            return (self.x1,self.y1)
        else:
            return (self.x2,self.y2)
        
    def getTail(self):
        if(self.direction == 'R' or self.direction == 'U'):
            return (self.x2,self.y2)
        else:
            return (self.x1,self.y1)
    
    def intersect(self, other):
        # parallel
        if self.up_down == other.up_down:
            return None
        
        # is intersect possible
        if self.up_down:
            if not ((other.x1 < self.x1 < other.x2) and 
                    (self.y1 < other.y1 < self.y2)):
                return None
        else:
            if not ((self.x1 < other.x1 < self.x2) and 
                    (other.y1 < self.y1 < other.y2)):
                return None
            
        if self.up_down:
            return [self.x1, other.y1]
        else:
            return [other.x1, self.y1]
        
    def numberOfSteps(self, cross):
        if self.up_down:
            tail = self.getHead()
            steps = abs(abs(tail[1])-abs(cross[1]))
        else:            
            tail = self.getHead()
            steps = abs(abs(tail[0])-abs(cross[0]))
        return steps
                 
def descriptionToWires(description):
    position = (0,0)
    wires = list()
    for step in description:
        direction = step[0]
        length = int(step[1:])
        new_line = line(position,direction,length)
        position = new_line.getTail()
        wires.append(new_line)
    return wires

def manhattan_dist(cross):
    return abs(cross[0]) + abs(cross[1])

def solve(wires):
    first_wire = descriptionToWires(wires[0].split(','))    
    second_wire = descriptionToWires(wires[1].split(','))
    closest_cross = sys.maxsize
    for line1 in first_wire:
        for line2 in second_wire:
            cross_at = line1.intersect(line2)
            if cross_at is not None:
                closest_cross = min(closest_cross,manhattan_dist(cross_at))

    return closest_cross

def solvePartTwo(wires):
    first_wire = descriptionToWires(wires[0].split(','))    
    second_wire = descriptionToWires(wires[1].split(','))
    sum_steps = sys.maxsize
    for i,line1 in enumerate(first_wire):
        for j,line2 in enumerate(second_wire):
            cross_at = line1.intersect(line2)
            if cross_at is not None:
                total1 = line1.numberOfSteps(cross_at) + sum([l.length for l in first_wire[:i]])
                total2 = line2.numberOfSteps(cross_at) + sum([l.length for l in second_wire[:j]])
                sum_steps = min(sum_steps, total1 + total2)
        
    return sum_steps

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solvePartTwo(puzzleInput)))

    