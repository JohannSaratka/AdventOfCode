'''
--- Day 10: Balance Bots ---
You come upon a factory in which many robots are zooming around 
handing small microchips to each other.
Upon closer examination, you notice that each bot only proceeds 
when it has two microchips, and once it does, it gives each one 
to a different bot or puts it in a marked "output" bin. Sometimes, 
bots take microchips from "input" bins, too.
Inspecting one of the microchips, it seems like they each contain 
a single number; the bots must use some logic to decide what to do 
with each chip. You access the local control computer and download 
the bots' instructions (your puzzle input).
Some of the instructions specify that a specific-valued microchip 
should be given to a specific bot; the rest of the instructions 
indicate what a given bot should do with its lower-value or 
higher-value chip.
'''
import unittest
import re

class TestGetSolution(unittest.TestCase):
    def setUp(self):
        self.solver = problemSolver()
        
    def test_function_solution1(self):
        self.assertEqual(self.solver.handleInstructions(['value 5 goes to bot 2', 
        'bot 2 gives low to bot 1 and high to bot 0',
        'value 3 goes to bot 1',
        'bot 1 gives low to output 1 and high to bot 0',
        'bot 0 gives low to output 2 and high to output 0',
        'value 2 goes to bot 2']), 1, "")

class Bot(object):
    def __init__(self):
        self.low=None
        self.high=None
        
    def giveLowChip(self,otherBot):
        otherBot.getChip(self.low)
        self.low=None
        
    def giveHighChip(self,otherBot):
        otherBot.getChip(self.high)
        self.high=None
        
    def getChip(self,chip):
        # move chip to free hand
        if self.high is None:
            self.high = chip
        else:
            self.low = chip
        # and swap if necessary
        if self.low > self.high:
            self.high, self.low = self.low, self.high
            
re.compile(pattern, flags)
class problemSolver(object):
    def __init__(self):
        self.botDict = dict()
        self.outputDict = dict()
            
    def handleInstructions(self,instrList):
        for instr in instrList:
            if instr.startswith("b"):
                
        return 0

if __name__ == '__main__':
    with open('DayXData.txt','r')as inputFile:
        solver = problemSolver()