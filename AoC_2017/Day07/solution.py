'''
Created on 01.12.2017

--- Day 6: Memory Reallocation ---

Part One
One program at the bottom supports the entire tower. It's holding a large disc, and on the 
disc are balanced several more sub-towers. At the bottom of these sub-towers, standing on 
the bottom disc, are other programs, each holding their own disc, and so on. At the very 
tops of these sub-sub-sub-...-towers, many programs stand simply keeping the disc below 
them balanced but with no disc of their own.
You offer to help, but first you need to understand the structure of these towers. You ask 
each program to yell out their name, their weight, and (if they're holding a disc) the names 
of the programs immediately above them balancing on that disc. You write this information 
down (your puzzle input). Unfortunately, in their panic, they don't do this in an orderly 
fashion; by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /     
         ugml - ebii
       /      \     
      |         jptl
      |        
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |             
      |         ktlj
       \      /     
         fwft - cntj
              \     
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft. 
Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up 
any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is 
much larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name of 
the bottom program?

Part Two
The programs explain the situation: they can't get down. Rather, they could get down, if they weren't 
expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong 
weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those 
sub-towers are supposed to be the same weight, or the disc itself isn't balanced. The weight of a 
tower is the sum of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all 
have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above 
it must each match. This means that the following sums must all be the same:

    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though 
the nodes above ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its 
stack to weigh 243 and keep the towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance 
the entire tower?
'''
import unittest
import re

class Test(unittest.TestCase):
    def testOne(self):
        with open("test_input.txt",'r') as testFile:
            self.assertEqual(solve(testFile.read().rstrip()), "tknk")
    def testTwo(self):
        with open("test_input.txt",'r') as testFile:
            self.assertEqual(solvePartTwo(testFile.read().rstrip()), 60)
        
def solve(input_list):
    reg_prog_info = re.compile(r'(\w+)\W*')
    list_bottom = list()
    list_holding = list()
    for line in input_list.split("\n"):
        prog_info = reg_prog_info.findall(line)
        if len(prog_info) > 2:
            list_bottom.append(prog_info[0])
            list_holding.extend(prog_info[2:])
    for program in list_bottom:
        if program not in list_holding:
            return program
         

def solvePartTwo(input_list):
    reg_prog_info = re.compile(r'(\w+)\W*')
    intial_weight = dict()
    top_level = dict()
    bottom_levels = dict()
    for line in input_list.split("\n"):
        prog_info = reg_prog_info.findall(line)
        intial_weight[prog_info[0]] = int(prog_info[1])
        if len(prog_info) > 2:
            bottom_levels[prog_info[0]]=(int(prog_info[1]),prog_info[2:])
        else:
            top_level[prog_info[0]] = int(prog_info[1])
    
    while len(bottom_levels) > 0:
        key, value = bottom_levels.popitem()
        if all(k in top_level.keys() for k in value[1]):
            weights_top = [top_level.pop(prog) for prog in value[1]]
            if weights_top[1:] == weights_top[:-1]:
                top_level[key] = value[0] + sum(weights_top)
            else:
                weight_unbalanced = min(weights_top,key=weights_top.count)
                weight_rest = max(weights_top,key=weights_top.count)
                name_unbalanced = value[1][weights_top.index(weight_unbalanced)]
                
                return intial_weight[name_unbalanced] + weight_rest - weight_unbalanced
        else:
            bottom_levels[key] = value
                
            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput),
            print solvePartTwo(puzzleInput)
    