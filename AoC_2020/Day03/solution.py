'''
--- Day 3: Toboggan Trajectory ---

With the toboggan login problems resolved, you set off toward the airport.
While travel by toboggan might be easy, it's certainly not safe: there's
very minimal steering and the area is covered in trees. You'll need to see
which angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer
coordinates in a grid. You make a map (your puzzle input) of the open
squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#

These aren't the only trees, though; due to something you read about once
involving arboreal genetics and biome stability, the same pattern repeats
to the right many times:
You start on the open square (.) in the top-left corner and need to reach the
bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper
model that prefers rational numbers); start by counting all the trees you
would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3
and down 1. Then, check the position that is right 3 and down 1 from there, and
so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where
there was an open square and X where there was a tree:
In this example, traversing the map using this slope would cause you to
encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3
and down 1, how many trees would you encounter?

--- Part Two ---

Time to check the rest of the slopes - you need to minimize the probability of
a sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following
slopes, you start at the top-left corner and traverse the map all the way to
the bottom:

    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.

In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s)
respectively; multiplied together, these produce the answer 336.

What do you get if you multiply together the number of trees encountered on
each of the listed slopes?

'''

import unittest


class Test(unittest.TestCase):
    tree_map = [
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#"]

    def test_solve_single_slope(self):
        self.assertEqual(solve(self.tree_map, 3, 1), 7)

    def test_solve_single_slop_skip_down(self):
        self.assertEqual(solve(self.tree_map, 1, 2), 2)

    def test_solve_all_slopes(self):
        self.assertEqual(solve_part_two(self.tree_map), 336)


def rotate(strg, n):
    rot = n % len(strg)
    return strg[rot:] + strg[:rot]


def solve(tree_map, right, down):
    slope = ""
    for num, tree_line in enumerate(tree_map):
        if num % down == 0:
            slope += rotate(tree_line, num // down * right)[0]
    return slope.count('#')


def solve_part_two(tree_map):
    answer = 1
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    for right, down in slopes:
        answer *= solve(tree_map, right, down)
    return answer


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput, 3, 1)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
