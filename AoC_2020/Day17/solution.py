'''
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical
Information Bureau at the North Pole contact you. They'd like some help
debugging a malfunctioning experimental energy source aboard one of their
super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of
Conway Cubes contained in a pocket dimension! When you hear it's having
problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer
3-dimensional coordinate (x,y,z), there exists a single cube which is either
active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive.
The only exception to this is a small flat region of cubes (your puzzle input);
the cubes in this region start in the specified active (#) or inactive (.)
state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where
any of their coordinates differ by at most 1. For example, given the cube at
x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at
x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the
following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active,
the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube
becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like you to
simulate the pocket dimension and determine what the configuration of cubes
should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state
represents a small 2-dimensional slice of it. (In particular, this initial
state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following
configurations, where the result of each cycle is shown layer-by-layer at each
given z coordinate (and the frame of view follows the active cells in each
cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the
active state.

Starting with your given initial configuration, simulate six cycles. How many
cubes are left in the active state after the sixth cycle?
'''

import unittest
import itertools
from typing import Tuple


class Test(unittest.TestCase):

    def test_boot_cycle(self):
        starting_map = [".#.",
                        "..#",
                        "###"]
        self.assertEqual(solve(starting_map), 112)

    def test_hyper_boot_cycle(self):
        starting_map = [".#.",
                        "..#",
                        "###"]
        self.assertEqual(solve_part_two(starting_map), 848)


class CubeMap(dict):
    def get_neighbor(self, axis):
        return (axis - 1, axis, axis + 1)

    def get_all_neighbors(self, cube):
        ''' get neighboring coordinates for all axis, i.e. (x-1, x, x+1)'''
        return tuple(self.get_neighbor(val) for val in cube)

    def get_candidates(self):
        candidates = set()
        for cube in self.keys():
            coords = self.get_all_neighbors(cube)
            candidates.update(set(itertools.product(*coords)))
        return candidates

    def check_active(self, cube):
        total = 0

        for neighbor_cube in itertools.product(*self.get_all_neighbors(cube)):
            if neighbor_cube == cube:
                # only neighbors are relevant
                continue
            total += bool(self.get(neighbor_cube))
            if total > 3:
                break

        if self.get(cube):
            # was active
            # stay active if it has 2 or 3 neighbors
            return bool(1 < total < 4)
        # was inactive
        # become active if there are exactly 3 neighbors
        return bool(total == 3)

    def simulate_cycle(self):
        active = list()
        inactive = list()
        for cube in self.get_candidates():
            is_active = self.check_active(cube)
            if is_active:
                active.append(cube)
            else:
                inactive.append(cube)

        for pos in inactive:
            if pos in self:
                del self[pos]
        for pos in active:
            self[pos] = True

    def run(self, num_cycles):
        for _ in range(num_cycles):
            self.simulate_cycle()


def solve(input_map):
    cube_dict = CubeMap()
    for y, line in enumerate(input_map):
        for x, pos in enumerate(line.strip()):
            if pos == '#':
                cube_dict[(x, y, 0)] = True

    cube_dict.run(6)
    return len(cube_dict)


def solve_part_two(input_map):
    cube_dict = CubeMap()
    for y, line in enumerate(input_map):
        for x, pos in enumerate(line.strip()):
            if pos == '#':
                cube_dict[(x, y, 0, 0)] = True

    cube_dict.run(6)
    return len(cube_dict)


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.readlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
