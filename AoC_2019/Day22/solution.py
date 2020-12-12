'''
--- Day 22: Slam Shuffle ---

There isn't much to do while you wait for the droids to repair your ship. At
least you're drifting in the right direction. You decide to practice a new card
shuffle you've been working on.

Digging through the ship's storage, you find a deck of space cards! Just like
any deck of space cards, there are 10007 cards in the deck numbered 0 through
10006. The deck must be new - they're still in factory order, with 0 on the
top, then 1, then 2, and so on, all the way through to 10006 on the bottom.

You've been practicing three different techniques that you use while shuffling.
Suppose you have a deck of only 10 cards (numbered 0 through 9):

To deal into new stack, create a new stack of cards by dealing the top card of
the deck onto the top of the new stack repeatedly until you run out of cards:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck
                      New stack

  1 2 3 4 5 6 7 8 9   Your deck
                  0   New stack

    2 3 4 5 6 7 8 9   Your deck
                1 0   New stack

      3 4 5 6 7 8 9   Your deck
              2 1 0   New stack

Several steps later...

                  9   Your deck
  8 7 6 5 4 3 2 1 0   New stack

                      Your deck
9 8 7 6 5 4 3 2 1 0   New stack

Finally, pick up the new stack you've just created and use it as the deck for
the next technique.

To cut N cards, take the top N cards off the top of the deck and move them as a
single unit to the bottom of the deck, retaining their order. For example, to
cut 3:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

      3 4 5 6 7 8 9   Your deck
0 1 2                 Cut cards

3 4 5 6 7 8 9         Your deck
              0 1 2   Cut cards

3 4 5 6 7 8 9 0 1 2   Your deck

You've also been getting pretty good at a version of this technique where N is
negative! In that case, cut (the absolute value of) N cards from the bottom of
the deck onto the top. For example, to cut -4:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

0 1 2 3 4 5           Your deck
            6 7 8 9   Cut cards

        0 1 2 3 4 5   Your deck
6 7 8 9               Cut cards

6 7 8 9 0 1 2 3 4 5   Your deck

To deal with increment N, start by clearing enough space on your table to lay
out all of the cards individually in a long line. Deal the top card into the
leftmost position. Then, move N positions to the right and deal the next card
there. If you would move into a position past the end of the space on your
table, wrap around and keep counting from the leftmost card again. Continue
this process until you run
'''
import unittest


class Test(unittest.TestCase):
    def test_deal_into_new_stack(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['deal into new stack']),
                         list(range(10 - 1, -1, -1)))

    def test_cut_positive(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['cut 3']),
                         [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

    def test_cut_negative(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['cut -4']),
                         [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

    def test_deal_with_increment(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['deal with increment 3']),
                         [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

    def test_all_1(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['deal with increment 7',
                                      'deal into new stack',
                                      'deal into new stack']),
                         [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

    def test_all_2(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['cut 6',
                                      'deal with increment 7',
                                      'deal into new stack']),
                         [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])

    def test_all_3(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['deal with increment 7',
                                      'deal with increment 9',
                                      'cut -2']),
                         [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])

    def test_all_4(self):
        self.assertEqual(slamShuffle(list(range(10)),
                                     ['deal into new stack',
                                      'cut -2',
                                      'deal with increment 7',
                                      'cut 8',
                                      'cut -4',
                                      'deal with increment 7',
                                      'cut 3',
                                      'deal with increment 9',
                                      'deal with increment 3',
                                      'cut -1']),
                         [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])


def slam_shuffle(deck, instructions):
    for instr in instructions:
        if instr.startswith('deal into'):
            deck.reverse()
        elif instr.startswith('cut'):
            _, value = instr.split(' ')
            deck = deck[int(value):]+deck[:int(value)]
        elif instr.startswith('deal with'):
            instr_split = instr.split(' ')
            value = int(instr_split[3])
            length = len(deck)
            new_deck = [0] * length
            for index, card in enumerate(deck):
                new_deck[(index * value) % length] = card
            deck = new_deck

    return deck


def solve(instructions):
    deck = slam_shuffle(list(range(10007)), instructions)

    return deck.index(2019)


def solve_part_two(int_code_prog):
    return False


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
