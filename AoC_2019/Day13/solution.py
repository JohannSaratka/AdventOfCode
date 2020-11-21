'''
--- Day 13: Care Package ---

As you ponder the solitude of space and the ever-increasing three-hour roundtrip for messages between you and Earth, you notice that the Space Mail Indicator Light is blinking. To help keep you sane, the Elves have sent you a care package.

It's a new game for the ship's cart cabinet! Unfortunately, the cart is all the way on the other end of the ship. Surely, it won't be hard to build your own - the care package even comes with schematics.

The cart cabinet runs Intcode software like the game the Elves sent (your puzzle input). It has a primitive draw_screen capable of drawing square tiles on a grid. The software draws tiles to the draw_screen with output instructions: every three output instructions specify the x position (distance from the left), y position (distance from the top), and tile id. The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the draw_screen when the game exits?

--- Part Two ---

The game didn't run because you didn't put in any quarters. Unfortunately, you did not bring any quarters. Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.

The cart cabinet has a joystick that can move left and right. The software reads the position of the joystick with input instructions:

    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.

The cart cabinet also has a segment display capable of showing a single number that represents the player's current score. When three output instructions specify X=-1, Y=0, the third output instruction is not a tile; the value instead specifies the new score to show in the segment display. For example, a sequence of output values like -1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the last block is broken?

'''
from collections import defaultdict
import pygame
from AoC_2019.common.ship_computer import CPU, intCodeToList
from AoC_2019.Day13.arcade import Arcade, WINDOWHEIGHT, WINDOWWIDTH


class Robot():
    def __init__(self, program):
        self.brain = CPU(program)
        self.brain.get_input = self.get_input
        self.brain.set_output = self.set_output
        self.grid = defaultdict(int)
        self.step = 0

    def get_input(self):
        return 0

    def set_output(self, out):
        if self.step == 0:
            self.out_x = out

        elif self.step == 1:
            self.out_y = out
        else:
            self.grid[(self.out_x, self.out_y)] = out
        self.step = (self.step + 1) % 3

    def draw_screen(self):
        grid_coords = self.grid.keys()
        max_x = max(grid_coords, key=lambda coord: coord[0])[0]
        max_y = max(grid_coords, key=lambda coord: coord[1])[1]
        hull_drawing = [''] * (max_y+1)
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if self.grid[(x, y)] == 1:
                    hull_drawing[y] += '#'
                elif self.grid[(x, y)] == 2:
                    hull_drawing[y] += 'X'
                elif self.grid[(x, y)] == 3:
                    hull_drawing[y] += '='
                elif self.grid[(x, y)] == 4:
                    hull_drawing[y] += 'O'
                else:
                    hull_drawing[y] += ' '
        return "\n".join(hull_drawing)


def solve(int_code_prog):
    cart = Robot(intCodeToList(int_code_prog))
    cart.brain.run()
    return len([tile for tile in cart.grid.values() if tile == 2])


def solve_part_two(int_code_prog):
    game = Arcade('Arcanoid',
                  (WINDOWWIDTH, WINDOWHEIGHT),
                  intCodeToList(int_code_prog))
    game.runGameLoop()

    return "See game output"


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: \n{}".format(solve_part_two(puzzleInput)))

