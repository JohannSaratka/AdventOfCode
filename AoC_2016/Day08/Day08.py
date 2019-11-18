'''
--- Day 8: Two-Factor Authentication ---
You come across a door implementing what you can only assume is an implementation of 
two-factor authentication after a long game of requirements telephone.
To get past the door, you first swipe a keycard (no problem; there was one on a 
nearby desk). Then, it displays a code on a little screen, and you type that code 
on a keypad. Then, presumably, the door unlocks.
Unfortunately, the screen has been smashed. After a few minutes, you've taken 
everything apart and figured out how it works. Now you just have to work out what 
the screen would have displayed.
The magnetic strip on the card you swiped encodes a series of instructions for the 
screen; these instructions are your puzzle input. The screen is 50 pixels wide and 
6 pixels tall, all of which start off, and is capable of three somewhat peculiar 
operations:
    rect AxB turns on all of the pixels in a rectangle at the top-left of the screen 
    which is A wide and B tall.
    rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right 
    by B pixels. Pixels that would fall off the right end appear at the left end of 
    the row.
    rotate column x=A by B shifts all of the pixels in column A (0 is the left column) 
    down by B pixels. Pixels that would fall off the bottom appear at the top of 
    the column.

'''
import unittest
import re
import numpy as np

class TestGetSolution(unittest.TestCase):
    def test_function_solution1(self):
        self.assertEqual(screenDriver(['rect 3x2']), 1, "")

turnOnPixelsRegex=re.compile(r"rect.(\d+)x(\d+)")
rotateRowRegex=re.compile(r".*y=(\d+)\D*(\d+)")
rotateColumnRegex=re.compile(r".*x=(\d+)\D*(\d+)")

def screenDriver(instructionSequence):
    screen=np.array([[0]*50]*6)
    for line in instructionSequence:
        match=turnOnPixelsRegex.match(line)
        if match:
            wide=int(match.group(1))
            tall=int(match.group(2))
            for y in xrange(tall):
                for x in xrange(wide):
                    screen[y,x]=1
            continue
        match=rotateRowRegex.match(line)
        if match:
            screen[int(match.group(1))]=np.roll(screen[int(match.group(1))],int(match.group(2)))
            continue
        match=rotateColumnRegex.match(line)
        if match:
            screen = np.transpose(screen)
            screen[int(match.group(1))]=np.roll(screen[int(match.group(1))],int(match.group(2)))
            screen = np.transpose(screen)
            continue
    return screen

if __name__ == '__main__':
    with open('Day08Data.txt','r')as inputFile:
        screen = screenDriver(inputFile.read().splitlines())
        print np.sum(screen)
        print screen
        '''TODO pretty print mit lambda
        [[# . . # . # # # . . . # # . . . . # # . # # # # . # . . . . # # # . . . # # . . # # # # . # # # # .]
         [# . . # . # . . # . # . . # . . . . # . # . . . . # . . . . # . . # . # . . # . # . . . . . . . # .]
         [# . . # . # . . # . # . . # . . . . # . # # # . . # . . . . # # # . . # . . . . # # # . . . . # . .]
         [# . . # . # # # . . # . . # . . . . # . # . . . . # . . . . # . . # . # . . . . # . . . . . # . . .]
         [# . . # . # . . . . # . . # . # . . # . # . . . . # . . . . # . . # . # . . # . # . . . . # . . . .]
         [. # # . . # . . . . . # # . . . # # . . # . . . . # # # # . # # # . . . # # . . # # # # . # # # # .]]
         '''