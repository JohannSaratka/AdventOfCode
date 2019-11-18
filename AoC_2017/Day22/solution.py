'''
Created on 01.12.2017

--- Day 22: Sporifica Virus ---

Diagnostics indicate that the local grid computing cluster has been contaminated with the Sporifica Virus. The grid computing cluster is a seemingly-infinite two-dimensional grid of compute nodes. Each node is either clean or infected by the virus.

To prevent overloading the nodes (which would render them useless to the virus) or detection by system administrators, exactly one virus carrier moves through the network, infecting or cleaning nodes as it moves. The virus carrier is always located on a single node in the network (the current node) and keeps track of the direction it is facing.

To avoid detection, the virus carrier works in bursts; in each burst, it wakes up, does some work, and goes back to sleep. The following steps are all executed in order one time each burst:

    If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done in-place; the current node does not change.)
    If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node is considered for the purposes of changing direction.)
    The virus carrier moves forward one node in the direction it is facing.

Diagnostics have also provided a map of the node infection status (your puzzle input). Clean nodes are shown as .; infected nodes are shown as #. This map only shows the center of the grid; there are many more nodes beyond those shown, but none of them are currently infected.

The virus carrier begins in the middle of the map facing up.
--- Part Two ---

As you go to remove the virus from the infected nodes, it evolves to resist your attempt.

Now, before it infects a clean node, it will weaken it to disable your defenses. If it encounters an infected node, it will instead flag the node to be cleaned in the future. So:

    Clean nodes become weakened.
    Weakened nodes become infected.
    Infected nodes become flagged.
    Flagged nodes become clean.

Every node is always in exactly one of the above states.

The virus carrier still functions in a similar way, but now uses the following logic during its bursts of action:

    Decide which way to turn based on the current node:
        If it is clean, it turns left.
        If it is weakened, it does not turn, and will continue moving in the same direction.
        If it is infected, it turns right.
        If it is flagged, it reverses direction, and will go back the way it came.
    Modify the state of the current node, as described above.
    The virus carrier moves forward one node in the direction it is facing.

Start with the same map (still using . for clean and # for infected) and still with the virus carrier starting in the middle and facing up.
'''
import unittest

class Test(unittest.TestCase):
     
    def testPartOne_SevenBursts(self):
        self.assertEqual(solve('..#\n#..\n...',7), 5)
    def testPartOne_SeventyBursts(self):
        self.assertEqual(solve('..#\n#..\n...',70), 41)
    def testPartOne_TenThousendBursts(self):
        self.assertEqual(solve('..#\n#..\n...',10000), 5587)
    def testPartTwo_FiveBursts(self):
        self.assertEqual(solvePartTwo('..#\n#..\n...',7), 1)
    def testPartTwo_OneHundredBursts(self):
        self.assertEqual(solvePartTwo('..#\n#..\n...',100), 26)
    def testPartTwo_TenMillionBursts(self):
        self.assertEqual(solvePartTwo('..#\n#..\n...',10000000), 2511944)
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
Directions = enum('UP','RIGHT','DOWN','LEFT')
moveDict={
         0: [0,-1],
         2: [0,1],
         3: [-1,0],
         1: [1,0],
         }
CLEAN = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'

def solve(input_map, num_bursts):
    num_infections = 0
    infection_map = [list(x) for x in input_map.split('\n')]
    map_width = len(infection_map[0])
    map_heigth = len(infection_map)
    virus_x = map_width / 2
    virus_y = map_heigth / 2
    virus_dir = Directions.UP
    
    for i in xrange(num_bursts):
        if infection_map[virus_y][virus_x] == INFECTED:
            virus_dir = (virus_dir + 1) % 4
            infection_map[virus_y][virus_x] = CLEAN
        else:
            virus_dir = (virus_dir - 1) % 4
            infection_map[virus_y][virus_x] = INFECTED
            num_infections += 1
            
        virus_x += moveDict[virus_dir][0]
        if virus_x < 0:
            virus_x = 0
            for row in infection_map:
                row.insert(0, CLEAN)
            map_width += 1
        elif virus_x >= map_width:
            for row in infection_map:
                row.append(CLEAN)
            map_width += 1
            
        virus_y += moveDict[virus_dir][1]
        if virus_y < 0:
            virus_y = 0
            infection_map.insert(0, [CLEAN for _ in xrange(map_width)])
            map_heigth += 1
        elif virus_y >= map_heigth:
            infection_map.append([CLEAN for _ in xrange(map_width)])
            map_heigth += 1
            
    return num_infections

def solvePartTwo(input_map, num_bursts):
    num_infections = 0
    infection_map = [list(x) for x in input_map.split('\n')]
    map_width = len(infection_map[0])
    map_heigth = len(infection_map)
    virus_x = map_width / 2
    virus_y = map_heigth / 2
    virus_dir = Directions.UP
    
    for i in xrange(num_bursts):
        if infection_map[virus_y][virus_x] == CLEAN:
            # clean - turn left becomes weak
            virus_dir -= 1
            infection_map[virus_y][virus_x] = WEAKENED
        
        elif infection_map[virus_y][virus_x] == WEAKENED:
            # weak - does not turn becomes infected
            infection_map[virus_y][virus_x] = INFECTED
            num_infections += 1
            
        elif infection_map[virus_y][virus_x] == INFECTED:
            # infected - turns right becomes flagged
            virus_dir += 1
            infection_map[virus_y][virus_x] = FLAGGED
        
        elif infection_map[virus_y][virus_x] == FLAGGED:
            # flagged - reverses becomes clean
            virus_dir += 2
            infection_map[virus_y][virus_x] = CLEAN
        virus_dir %= 4
            
        virus_x += moveDict[virus_dir][0]
        if virus_x < 0:
            virus_x = 0
            for row in infection_map:
                row.insert(0, CLEAN)
            map_width += 1
        elif virus_x >= map_width:
            for row in infection_map:
                row.append(CLEAN)
            map_width += 1
            
        virus_y += moveDict[virus_dir][1]
        if virus_y < 0:
            virus_y = 0
            infection_map.insert(0, [CLEAN for _ in xrange(map_width)])
            map_heigth += 1
        elif virus_y >= map_heigth:
            infection_map.append([CLEAN for _ in xrange(map_width)])
            map_heigth += 1
  
    return num_infections
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:           
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput,10000)
            print solvePartTwo(puzzleInput,10000000)