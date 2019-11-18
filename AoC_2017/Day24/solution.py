'''
Created on 01.12.2017

--- Day 24: Electromagnetic Moat ---

The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from the side of the building at regular intervals and descend down into the void. There's no way to cross, but you need to get inside.

No way, of course, other than building a bridge out of the magnetic components strewn about nearby.

Each component has two ports, one on each end. The ports come in all different types, and only matching types can be connected. You take an inventory of the components by their port types (your puzzle input). Each port is identified by the number of pins it uses; more pins mean a stronger connection for your bridge. A 3/7 component, for example, has a type-3 port on one side, and a type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic, zero-pin port. Because of this, the first port you use must be of type 0. It doesn't matter what type of port you end with; your goal is just to make the bridge as strong as possible.

The strength of a bridge is the sum of the port types in each component. For example, if your bridge is made of components 0/3, 3/7, and 7/4, your bridge has a strength of 0+3 + 3+7 + 7+4 = 24.
--- Part Two ---

The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

Of them, the one which uses the 3/5 component is stronger; its strength is 0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick the strongest one.

'''
import unittest

class Test(unittest.TestCase):
     
    def testPartOne(self):
        self.assertEqual(solve('0/2\n2/2\n2/3\n3/4\n3/5\n0/1\n10/1\n9/10'), 31)
    def testPartTwo(self):
        self.assertEqual(solvePartTwo('0/2\n2/2\n2/3\n3/4\n3/5\n0/1\n10/1\n9/10'), 19)

def solve(input_list):
    dominos = list()
    for item in input_list.split('\n'):
        item1,item2 = item.split('/')
        dominos.append([int(item1),int(item2)])
    max_strength = 0
    for start in [x for x in dominos if x[0] == 0]:
        max_strength = max(max_strength,findStrongestBridge(start[1],[x for x in dominos if x!=start]))
    return max_strength
    
def findStrongestBridge(start_port, component_list):
    strength = 0
    valid_options_left = [x for x in component_list if x[0] == start_port]
    valid_options_right = [x for x in component_list if x[1] == start_port]
    
    if len(valid_options_left)==0 and len(valid_options_right)==0:
        return start_port
    
    for start_left in valid_options_left:
        strength = max(strength,findStrongestBridge(start_left[1], [x for x in component_list if x != start_left]))
    
    for start_right in valid_options_right:
        strength = max(strength,findStrongestBridge(start_right[0], [x for x in component_list if x != start_right]))
        
    return (strength + 2*start_port)

def findLongestBridge(start_port, component_list, strength, depth):
    strength += 2*start_port
    max_depth = 0
    max_strength = 0
    valid_options_left = [x for x in component_list if x[0] == start_port]
    valid_options_right = [x for x in component_list if x[1] == start_port]
     
    if len(valid_options_left)==0 and len(valid_options_right)==0:
        return (strength - start_port, depth)
     
    for start_left in valid_options_left:
        new_strength, new_depth = findLongestBridge(start_left[1], [x for x in component_list if x != start_left], strength, depth + 1)
        if new_depth > max_depth:
            max_depth = new_depth
            max_strength = new_strength
        elif new_depth==max_depth:
            max_strength = max(new_strength,max_strength)

        
    for start_right in valid_options_right:
        new_strength, new_depth = findLongestBridge(start_right[0], [x for x in component_list if x != start_right], strength, depth + 1)
        if new_depth > max_depth:
            max_depth = new_depth
            max_strength = new_strength
        elif new_depth==max_depth:
            max_strength = max(new_strength,max_strength)
        
    return (max_strength,max_depth)
       
def solvePartTwo(input_list):
    dominos = list()
    for item in input_list.split('\n'):
        item1,item2 = item.split('/')
        dominos.append([int(item1),int(item2)])
    max_strength = 0
    max_depth = 0
    for start in [x for x in dominos if x[0] == 0]:
        new_strength,new_depth = max(max_strength,findLongestBridge(start[1],[x for x in dominos if x != start],start[0],0))
        if new_depth > max_depth:
            max_depth = new_depth
            max_strength = new_strength
        elif new_depth==max_depth:
            max_strength = max(new_strength,max_strength)
    return max_strength
  
          
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:           
            puzzleInput = inFile.read().rstrip()
            #print solve(puzzleInput)
            print solvePartTwo(puzzleInput)