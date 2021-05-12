'''
---- Day 12: Rain Risk ---

Your ferry made decent progress toward the island, but the storm came in faster
than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning;
rather than giving a route directly to safety, it produced extremely circuitous
instructions. When the captain uses the PA system to ask if anyone can help,
you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of
single-character actions paired with integer input values. After staring at
them for a few minutes, you work out what they probably mean:

    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship
is currently facing.

The ship starts by facing east. Only the L and R actions change the direction
the ship is facing. (That is, if the ship is facing east and the next
instruction is N10, the ship would move north 10 units, but would still move
east if the following action were F.)

For example:

F10
N3
F7
R90
F11

These instructions would be handled as follows:

    F10 would move the ship 10 units east (because the ship starts by facing
east) to east 10, north 0.
    N3 would move the ship 3 units north to east 10, north 3.
    F7 would move the ship another 7 units east (because the ship is still
facing east) to east 17, north 3.
    R90 would cause the ship to turn right by 90 degrees and face south; it
remains at east 17, north 3.
    F11 would move the ship 11 units south to east 17, south 8.

At the end of these instructions, the ship's Manhattan distance (sum of the
absolute values of its east/west position and its north/south position) from
its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan
distance between that location and the ship's starting position?

--- Part Two ---

Before you can give the destination to the captain, you realize that the actual
action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to
the ship's position:

    Action N means to move the waypoint north by the given value.
    Action S means to move the waypoint south by the given value.
    Action E means to move the waypoint east by the given value.
    Action W means to move the waypoint west by the given value.
    Action L means to rotate the waypoint around the ship left (counter-
clockwise) the given number of degrees.
    Action R means to rotate the waypoint around the ship right (clockwise) the
given number of degrees.
    Action F means to move forward to the waypoint a number of times equal to
the given value.

The waypoint starts 10 units east and 1 unit north relative to the ship. The
waypoint is relative to the ship; that is, if the ship moves, the waypoint
moves with it.

For example, using the same instructions as above:

    F10 moves the ship to the waypoint 10 times (a total of 100 units east and
10 units north), leaving the ship at east 100, north 10. The waypoint stays 10
units east and 1 unit north of the ship.
    N3 moves the waypoint 3 units north to 10 units east and 4 units north of
the ship. The ship remains at east 100, north 10.
    F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28
units north), leaving the ship at east 170, north 38. The waypoint stays 10
units east and 4 units north of the ship.
    R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to
4 units east and 10 units south of the ship. The ship remains at east 170,
north 38.
    F11 moves the ship to the waypoint 11 times (a total of 44 units east and
110 units south), leaving the ship at east 214, south 72. The waypoint stays 4
units east and 10 units south of the ship.

After these operations, the ship's Manhattan distance from its starting
position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the
Manhattan distance between that location and the ship's starting position?
'''

import unittest
from enum import IntEnum, auto
from dataclasses import dataclass


class Test(unittest.TestCase):
    def test_instructions_part_one(self):
        navigation = ["F10", "N3", "F7", "R90", "F11"]
        self.assertEqual(solve(navigation), 25)

    def test_instructions_part_two(self):
        navigation = ["F10", "N3", "F7", "R90", "F11"]
        self.assertEqual(solve_part_two(navigation), 286)

    def test_instructions_back_to_the_start(self):
        navigation = [
            "F10",
            "R180",
            "F20",
            "L180",
            "F20",
            "R90",
            "R90",
            "F20",
            "L90",
            "L90",
            "F10"]
        self.assertEqual(solve_part_two(navigation), 0)


class Direction(IntEnum):
    NORTH = 0
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


@dataclass
class Point():
    x: int
    y: int

    def rotate_left(self, value):
        if value == 90:
            self.x, self.y = -self.y, self.x
        elif value == 180:
            self.x, self.y = -self.x, -self.y
        elif value == 270:
            self.x, self.y = self.y, -self.x

    def rotate_right(self, value):
        self.rotate_left(360 - value)


class Ship():
    def __init__(self):
        self.facing = Direction.EAST
        self.position = Point(0, 0)

    def execute(self, command):
        action = command[0]
        value = int(command[1:])
        if action in ['N', 'E', 'S', 'W']:
            self.move(action, value)
        elif action == 'F':
            self.move(['N', 'E', 'S', 'W'][self.facing.value], value)
        elif action == 'L':
            self.facing = Direction((self.facing.value - value / 90) % 4)
        elif action == 'R':
            self.facing = Direction((self.facing.value + value / 90) % 4)

    def move(self, action, value):
        if action == 'N':
            self.position.y += value
        elif action == 'S':
            self.position.y -= value
        elif action == 'E':
            self.position.x += value
        elif action == 'W':
            self.position.x -= value

    def get_distance(self):
        return abs(self.position.x) + abs(self.position.y)


class ShipTwo(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint = Point(10, 1)

    def execute(self, command):
        action = command[0]
        value = int(command[1:])
        if action == 'N':
            self.waypoint.y += value
        elif action == 'S':
            self.waypoint.y -= value
        elif action == 'E':
            self.waypoint.x += value
        elif action == 'W':
            self.waypoint.x -= value
        elif action == 'F':
            self.position.x += self.waypoint.x * value
            self.position.y += self.waypoint.y * value
        elif action == 'L':
            self.waypoint.rotate_left(value)
        elif action == 'R':
            self.waypoint.rotate_right(value)
#         print(f"{command}: Pos({self.position.x}, {self.position.y})"
#               f" Waypoint({self.waypoint.x}, {self.waypoint.y})")


def solve(navigation):
    ferry = Ship()
    for command in navigation:
        ferry.execute(command)

    return ferry.get_distance()


def solve_part_two(navigation):
    ferry = ShipTwo()
    for command in navigation:
        ferry.execute(command)

    return ferry.get_distance()


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
