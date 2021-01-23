'''
--- Day 10: Elves Look, Elves Say ---

Today, the Elves are playing a game called look-and-say. They take turns making
sequences by reading aloud the previous sequence and using that reading as the
next sequence. For example, 211 is read as "one two, two ones", which becomes
1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as
input for the next step. For each step, take the previous value, and replace
each run of digits (like 111) with the number of digits (3) followed by the
digit itself (1).

For example:

    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40 times.
What is the length of the result?
--- Part Two ---

Neat, right? You might also enjoy hearing John Conway talking about this
sequence (that's Conway of Conway's Game of Life fame).

Now, starting again with the digits in your puzzle input, apply this process 50
times. What is the length of the new result?

'''

import unittest


class Test(unittest.TestCase):

    def test_look_and_say(self):
        self.assertEqual(look_and_say("1"), "11")
        self.assertEqual(look_and_say("11"), "21")
        self.assertEqual(look_and_say("21"), "1211")
        self.assertEqual(look_and_say("1211"), "111221")
        self.assertEqual(look_and_say("111221"), "312211")

    def test_total_length_is_correct(self):
        self.assertEqual(solve("1", 5), 6)


def look_and_say(sequence):
    current = sequence[0]
    return_seq = ""
    count = 0
    for c in sequence:
        if c is current:
            count += 1
        else:
            return_seq += str(count) + current
            count = 1
            current = c
    return_seq += str(count) + c
    return return_seq


def solve(start_seq, steps=40):
    sequence = start_seq
    for _ in range(steps):
        sequence = look_and_say(sequence)
    return len(sequence)


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput[0])))
        print("Solution Part 2: {}".format(solve(puzzleInput[0], 50)))
