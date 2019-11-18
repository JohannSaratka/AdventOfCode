'''
Created on 01.12.2017

--- Day 13: Packet Scanners ---

You need to cross a vast firewall. The firewall consists of several layers, each with a security scanner that moves back and forth across the layer. To succeed, you must not be detected by a scanner.

By studying the firewall briefly, you are able to record (in your puzzle input) the depth of each layer and the range of the scanning area for the scanner within it, written as depth: range. Each layer has a thickness of exactly 1. A layer at depth 0 begins immediately inside the firewall; a layer at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4

This means that there is a layer immediately inside the firewall (with range 3), a second layer immediately after that (with range 2), a third layer which begins at depth 4 (with range 4), and a fourth layer which begins at depth 6 (also with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Within each layer, a security scanner moves back and forth within its range. Each security scanner starts at the top and moves down until it reaches the bottom, then moves up until it reaches the top, and repeats. A security scanner takes one picosecond to move one step.
Your plan is to hitch a ride on a packet about to move through the firewall. The packet will travel along the top of each layer, and it moves at one layer per picosecond. Each picosecond, the packet moves one layer forward (its first move takes it into layer 0), and then the scanners move one step. If there is a scanner at the top of the layer as your packet enters it, you are caught. (If a scanner moves into the top of its layer while you are there, you are not caught: it doesn't have time to notice you before you leave.)

--- Part Two ---

Now, you need to pass through the firewall without being caught - easier said than done.

You can't control the speed of the packet, but you can delay it any number of picoseconds. For each picosecond you delay the packet before beginning your trip, all security scanners move one step. You're not in the firewall during this time; you don't enter layer 0 until you stop delaying the packet.
Because all smaller delays would get you caught, the fewest number of picoseconds you would need to delay to get through safely is 10.

What is the fewest number of picoseconds that you need to delay the packet to pass through the firewall without being caught?
'''
import unittest
from time import time

class Test(unittest.TestCase):
    def testNoDelay(self):
        test_data ='0: 3\n1: 2\n4: 4\n6: 4'
        self.assertEqual(solve(test_data), 24)
        
    def testZeroSeverity(self):
        test_data ='0: 3\n1: 2\n4: 4\n6: 4'
        self.assertEqual(solvePartTwo(test_data), 10)

def solve(input_list):
    firewall_list = [map(int,item.split(': '))for item in input_list.split('\n')]
    return calulate_severity(firewall_list)

def calulate_severity(firewalls,start_delay = 0):
    severity = 0
    for depth, scanner_range in firewalls:        
        player_pos = depth + start_delay
        trim_pos = player_pos % (2 * (scanner_range - 1))
        scanner_pos = trim_pos if trim_pos < scanner_range  else trim_pos - (trim_pos % scanner_range+1)
        if scanner_pos == 0:
            severity += depth * scanner_range
            if start_delay != 0:
                severity = 1 # early exit for part two
                break
    return severity

def solvePartTwo(input_list):
    n = 0
    firewall_list = [map(int,item.split(': '))for item in input_list.split('\n')]
    while True:
        if calulate_severity(firewall_list, n) == 0:
            return n
        n += 1
    
            
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()        
            print solve(puzzleInput)
            start = time()
            print solvePartTwo(puzzleInput)
            print('Completed in ' + str(time() - start) + ' seconds.')