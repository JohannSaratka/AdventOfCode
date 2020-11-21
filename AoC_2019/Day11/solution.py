'''
--- Day 11: Space Police ---

On the way to Jupiter, you're pulled over by the Space Police.

"Attention, unmarked spacecraft! You are in violation of Space Law! All spacecraft must have a clearly visible registration identifier! You have 24 hours to comply or be sent to Space Jail!"

Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it takes almost three hours for their reply signal to reach you, they send instructions for how to power up the emergency hull painting robot and even provide a small Intcode program (your puzzle input) that will cause it to paint your ship appropriately.

There's just one problem: you don't have an emergency hull painting robot.

You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or white. (All of the panels are currently black.)

The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

    First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
    Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.

After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode computer inside the robot during this process.

For example, suppose the robot is about to start running. Drawing black panels as ., white panels as #, and the robot pointing the direction it is facing (< ^ > v), the initial state and region near the robot looks like this:

.....
.....
..^..
.....
.....

The panel under the robot (not visible here because a ^ is shown instead) is also black, and so any input instructions at this point should be provided 0. Suppose the robot eventually outputs 1 (paint white) and then 0 (turn left). After taking these actions and moving forward one panel, the region now looks like this:

.....
.....
.<#..
.....
.....

Input instructions should still be provided 0. Next, the robot might output 0 (paint black) and then 0 (turn left):

.....
.....
..#..
.v...
.....

After more outputs (1,0, 1,0):

.....
.....
..^..
.##..
.....

The robot is now back where it started, but because it is now on a white panel, input instructions should be provided 1. After several more outputs (0,1, 1,0, 1,0), the area looks like this:

.....
..<#.
...#.
.##..
.....

Before you deploy the robot, you should probably have an estimate of the area it will cover: specifically, you need to know the number of panels it paints at least once, regardless of color. In the example above, the robot painted 6 panels at least once. (It painted its starting panel twice, but that panel is still only counted once; it also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at least once?

--- Part Two ---

You're not sure what it's trying to paint, but it's definitely not a registration identifier. The Space Police are getting impatient.

Checking your external ship cameras again, you notice a white panel marked "emergency hull painting robot starting panel". The rest of the panels are still black, but it looks like the robot was expecting to start on a white panel, not a black one.

Based on the Space Law Space Brochure that the Space Police attached to one of your windows, a valid registration identifier is always eight capital letters. After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?

'''

from AoC_2019.common.ship_computer import CPU, intCodeToList
from collections import defaultdict
from enum import IntFlag
import unittest

class Test(unittest.TestCase):
    def testRobotTurnLeft(self):
        testRobot = Robot([0])
        testRobot.turn(0)
        self.assertEqual(testRobot.direction, Direction.LEFT)        
        testRobot.turn(0)
        self.assertEqual(testRobot.direction, Direction.DOWN)        
        testRobot.turn(0)
        self.assertEqual(testRobot.direction, Direction.RIGHT)        
        testRobot.turn(0)
        self.assertEqual(testRobot.direction, Direction.UP)
        
    def testRobotTurnRight(self):
        testRobot = Robot([0])
        testRobot.turn(1)
        self.assertEqual(testRobot.direction, Direction.RIGHT)
        testRobot.turn(1)
        self.assertEqual(testRobot.direction, Direction.DOWN)        
        testRobot.turn(1)
        self.assertEqual(testRobot.direction, Direction.LEFT)
        testRobot.turn(1)
        self.assertEqual(testRobot.direction, Direction.UP)
        
class Direction(IntFlag):
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    
    def __rshift__(self, other):
        if self.value >> other == 0:
            return Direction(8)
        return Direction(self.value >> other)
    
    def __lshift__(self, other):
        if self.value << other == 16:
            return Direction(1)
        return Direction(self.value << other)
    
class Robot(object):
    def __init__(self, program, initial_panel = 0):
        self.brain = CPU(program)
        self.brain.get_input = self.provide_panel
        self.brain.set_output = self.set_output
        self.ship_hull = defaultdict(int)
        self.direction = Direction.UP
        self.pos = [0,0]
        self.paint(initial_panel)
        self.step = 0
        
    def provide_panel(self):
        return self.ship_hull[(self.pos[0], self.pos[1])]
    
    def set_output(self,out):
        if self.step == 0:
            self.paint(out)
            self.step = 1
        else:
            self.turn(out)
            self.move()
            self.step = 0
        
    def turn(self,rot):
        if rot == 0:
            self.direction >>= 1
        else:
            self.direction <<= 1
            
    def paint(self, color):
        self.ship_hull[(self.pos[0], self.pos[1])] = color
    
    def move(self):
        if self.direction == Direction.UP:
            self.pos[1] -= 1
        elif self.direction == Direction.RIGHT:
            self.pos[0] += 1
        elif self.direction == Direction.DOWN:
            self.pos[1] += 1
        elif self.direction == Direction.LEFT:
            self.pos[0] -= 1
            
    def draw_screen(self):
        hull_coords = self.ship_hull.keys()
        max_x = max(hull_coords, key = lambda coord: coord[0])[0]
        max_y = max(hull_coords, key = lambda coord: coord[1])[1]
        hull_drawing = [''] * (max_y+1)
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if self.ship_hull[(x,y)] == 1:
                    hull_drawing[y] += '#'
                else:
                    hull_drawing[y] += ' '
        return ("\n".join(hull_drawing))
    
def solve(intCodeProg): 
    hull_painter = Robot(intCodeToList(intCodeProg))
    hull_painter.brain.run()
    return len(hull_painter.ship_hull.keys())

def solvePartTwo(intCodeProg):
    hull_painter = Robot(intCodeToList(intCodeProg), 1)
    hull_painter.brain.run()
    return hull_painter.draw_screen()

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: \n{}".format(solvePartTwo(puzzleInput)))

    