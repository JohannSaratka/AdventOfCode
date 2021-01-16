'''
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided
him the distances between every pair of locations. He can start and end at any
two (different) locations he wants, but he must visit each location exactly
once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the answer
is 605 in this example.

What is the distance of the shortest route?
'''

import unittest
from collections import defaultdict
from itertools import combinations, permutations


class Test(unittest.TestCase):

    def test_simple_count(self):
        dist_pairs = [
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141"]

        self.assertEqual(solve(dist_pairs), (605, 982))


def create_distance_dictionary(dist_pairs):
    dist_dict = defaultdict(lambda: defaultdict(int))
    for pair in dist_pairs:
        start, _, end, _, dist = pair.split(" ")
        start_dict = dist_dict[start]
        start_dict[end] = int(dist)
        end_dict = dist_dict[end]
        end_dict[start] = int(dist)
    return dist_dict


def calculate_total_distance(route, dist_dict):
    total = 0
    for i, town in enumerate(route):
        if i < len(route) - 1:
            next_town = route[i + 1]
            total += dist_dict[town][next_town]
    return total


def solve(dist_pairs):
    dist_dict = create_distance_dictionary(dist_pairs)
    towns = dist_dict.keys()

    # init with value larger/ smaller than any possible total distance
    min_total = 1000 * len(towns)
    max_total = 0

    for route in permutations(towns, len(towns)):
        total = calculate_total_distance(route, dist_dict)
        min_total = min(min_total, total)
        max_total = max(max_total, total)
    return min_total, max_total


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution: {}".format(solve(puzzleInput)))
