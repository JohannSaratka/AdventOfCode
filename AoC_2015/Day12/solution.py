'''
--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order.
Unfortunately, their accounting software uses a peculiar storage format. That's
where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]),
objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply
find all of the numbers throughout the document and add them together.

For example:

    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything
red.

Ignore any object (and all of its children) which has any property with the
value "red". Do this only for objects ({...}), not arrays ([...]).

    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is
    ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire
    structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.

'''

import unittest
import json


class Test(unittest.TestCase):
    def test_sum_of_all_numbers(self):
        self.assertEqual(solve('[1,2,3]'), 6)
        self.assertEqual(solve('{"a":2,"b":4}'), 6)
        self.assertEqual(solve('[[[3]]]'), 3)
        self.assertEqual(solve('{"a":{"b":4},"c":-1}'), 3)
        self.assertEqual(solve('15'), 15)
        self.assertEqual(solve('{"a":[-1,1]}'), 0)
        self.assertEqual(solve('[-1,{"a":1}]'), 0)
        self.assertEqual(solve('[]{}'), 0)

    def test_ignore_red_property(self):
        self.assertEqual(solve_part_two('[1,2,3]'), 6)
        self.assertEqual(solve_part_two('[1,{"c":"red","b":2},3]'), 4)
        self.assertEqual(solve_part_two('{"d":"red","e":[1,2,3,4],"f":5}'), 0)
        self.assertEqual(solve_part_two('[1,"red",5]'), 6)


def solve(document):
    chars = '{}[],":'
    for c in chars:
        document = document.replace(c, ' ')
    numbers = [int(s) for s in document.split() if not s.isalpha()]
    return sum(numbers)


def get_sum(json_obj):
    if isinstance(json_obj, int):
        return json_obj
    elif isinstance(json_obj, str):
        return 0
    elif isinstance(json_obj, list):
        total = 0
        for element in json_obj:
            total += get_sum(element)
        return total
    elif isinstance(json_obj, dict):
        total = 0
        for value in json_obj.values():
            if value == "red":
                return 0
            else:
                total += get_sum(value)
        return total


def solve_part_two(document):
    test = json.loads(document)
    return get_sum(test)


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzle_input = inFile.read().splitlines()[0]
        print(f"Solution Part 1: {solve(puzzle_input)}")
        print(f"Solution Part 2: {solve_part_two(puzzle_input)}")
