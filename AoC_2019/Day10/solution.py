'''
--- Day 10: Monitoring Station ---

You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).

The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##

The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:

.7..7
.....
67775
....7
...87

Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would be blocked and could not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c

Here are some larger examples:

    Best is 5,8 with 33 other asteroids detected:

    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####

    Best is 1,2 with 35 other asteroids detected:

    #.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.

    Best is 6,3 with 41 other asteroids detected:

    .#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..

    Best is 11,13 with 210 other asteroids detected:

    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##

Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

'''
import unittest
from collections import namedtuple, defaultdict
import math


class Test(unittest.TestCase):
    def testSmallMap(self):
        self.assertEqual(solve([
            '.#..#',
            '.....',
            '#####',
            '....#',
            '...##'
            ]), 8)
        
    def testMiddleMap1(self):
        self.assertEqual(solve([
            '......#.#.',
            '#..#.#....',
            '..#######.',
            '.#.#.###..',
            '.#..#.....',
            '..#....#.#',
            '#..#....#.',
            '.##.#..###',
            '##...#..#.',
            '.#....####',
            ]), 33)
        
    def testMiddleMap2(self):
        self.assertEqual(solve([
            '#.#...#.#.',
            '.###....#.',
            '.#....#...',
            '##.#.#.#.#',
            '....#.#.#.',
            '.##..###.#',
            '..#...##..',
            '..##....##',
            '......#...',
            '.####.###.',
            ]), 35)
        
    def testMiddleMap3(self):
        self.assertEqual(solve([
            '.#..#..###',
            '####.###.#',
            '....###.#.',
            '..###.##.#',
            '##.##.#.#.',
            '....###..#',
            '..#.#..#.#',
            '#..#.#.###',
            '.##...##.#',
            '.....#.#..',
            ]), 41)
    largeInputMap = [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##',
        ]
    def testLargeMap(self):
        self.assertEqual(solve(self.largeInputMap), 210)
        
    def testLargeMapPart2(self):
        self.assertEqual(solvePartTwo(self.largeInputMap), 802)
        
    def testGetAngle(self):
        vaporization_order = create_vaporization_order(self.largeInputMap)
        expected=[(1,11,12),
                  (2,12,1),
                  (3,12,2),
                  (10,12,8),
                  (20,16,0),
                  (50,16,9),
                  (100,10,16),
                  (199,9,6),
                  (200,8,2),
                  (201,10,9),
            ]
        for nth_asteroid,x,y in expected:
            self.assertEqual(vaporization_order[nth_asteroid - 1], Asteroid(x,y))
        
Asteroid = namedtuple('Asteroid',('x y'))


def distance(first, second):
    return abs(first.x - second.x) + abs(first.y - second.y)

def detect(monitoring_station, asteroid_positions):
    other_asteroids = sorted(asteroid_positions, key = lambda asteroid: distance(monitoring_station, asteroid))
    line_of_sight = defaultdict(list)
    for obj in other_asteroids[1:]:
        dx = monitoring_station.x - obj.x
        dy = monitoring_station.y - obj.y
        denom = math.gcd(dx,dy)
        line_of_sight[(dx // denom, dy // denom)].append(obj)
        
    return line_of_sight
    

def create_asteroid_positions(asteroid_map):
    asteroid_list = list()
    for y, row in enumerate(asteroid_map):
        for x, pos in enumerate(row):
            if pos == '#':
                asteroid_list.append(Asteroid(x, y))
    
    return asteroid_list

def solve(asteroid_map):
    asteroid_list = create_asteroid_positions(asteroid_map)
    monitoring_station = max(asteroid_list,key = lambda asteroid: len(detect(asteroid, asteroid_list)))
    return len(detect(monitoring_station, asteroid_list))

def get_angle(first,second):
    a = second.y - first.y
    b = first.x - second.x
    c = math.sqrt(a*a + b*b)
    if b >= 0:
        return math.acos(a/c)
    else:
        return (2 * math.pi) - math.acos(a/c)
    

def create_vaporization_order(asteroid_map):
    asteroid_list = create_asteroid_positions(asteroid_map)
    monitoring_station = max(asteroid_list, key = lambda asteroid: len(detect(asteroid, asteroid_list)))
    # get list of directly detectable asteroids and sort by rotation angle
    # to account for multiple rotations is unnecessary since this list will have more than 200 elements
    detectable = detect(monitoring_station, asteroid_list)
    detectable = [t[0] for t in detectable.values()]
    detectable.sort(key = lambda arg: get_angle(arg, monitoring_station))
    
    return detectable

def solvePartTwo(asteroid_map):
    final_vaporization_list = create_vaporization_order(asteroid_map)
    asteroid_200 = final_vaporization_list[200 - 1]
    return asteroid_200[0]*100 + asteroid_200[1]

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solvePartTwo(puzzleInput)))

    