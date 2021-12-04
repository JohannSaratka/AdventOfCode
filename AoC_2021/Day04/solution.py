'''
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however, is
a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on
which it appears. (Numbers may not appear on all boards.) If all numbers in any
row or any column of a board are marked, that board wins. (Diagonals don't
count.)

The submarine has a bingo subsystem to help passengers (currently, you and the
giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each
other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are
still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or
column of marked numbers (in this case, the entire top row is marked: 14 21 17
24 4).

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board; in this case, the sum is 188. Then,
multiply that sum by the number that was just called when the board won, 24, to
get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?

--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure out
which board will win last and choose that one. That way, no matter which boards
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after
13 is eventually called and its middle column is completely marked. If you were
to keep playing until this point, the second board would have a sum of unmarked
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score
be?
'''

import unittest


class Test(unittest.TestCase):
    def test_final_score_earliest(self):
        with open("test_input.txt", 'r') as in_file:
            test_input = in_file.read().splitlines()
        self.assertEqual(solve(test_input), 4512)

    board = ["22 13 17 11  0",
             " 8  2 23  4 24",
             "21  9 14 16  7",
             " 6 10  3 18  5",
             " 1 12 20 15 19"]

    def test_create_board(self):
        card = BingoBoard(self.board)
        self.assertEqual(card.rows[1], [8, 2, 23, 4, 24])
        self.assertEqual(card.cols[1], [13, 2, 9, 10, 12])

    def test_find_earliest_bingo(self):
        card = BingoBoard(self.board)
        bingo_numbers = {key: val for (val, key) in enumerate(range(25))}
        self.assertEqual(card.find_earliest_bingo(bingo_numbers), 13)

    def test_calculate_score(self):
        card = BingoBoard(self.board)
        bingo_numbers = {key: val for (val, key) in enumerate(range(25))}
        card.find_earliest_bingo(bingo_numbers)
        self.assertEqual(card.calculate_score(13), 2717)

    def test_final_score_latest(self):
        with open("test_input.txt", 'r') as in_file:
            test_input = in_file.read().splitlines()
        self.assertEqual(solve_part_two(test_input), 1924)


class BingoBoard():
    def __init__(self, board_list):
        self.rows = []
        self.mark_rows = []
        self.cols = [[]for _ in range(5)]
        self.mark_cols = []
        for ind, row in enumerate(board_list):
            self.rows.append([int(x) for x in row.split()])
            for ind_col, val in enumerate(self.rows[ind]):
                self.cols[ind_col].append(val)

        self.winning_pos = 0

    def find_earliest_bingo(self, bingo_numbers):
        # for each board (row and column) calculate earliest possible bingo
        self.mark_rows = [[bingo_numbers[x]
                           for x in self.rows[i]]for i in range(5)]
        self.mark_cols = [[bingo_numbers[x]
                           for x in self.cols[i]]for i in range(5)]
        earliest_row = min([max(row) for row in self.mark_rows])
        earliest_col = min([max(col) for col in self.mark_cols])
        self.winning_pos = min(earliest_row, earliest_col)
        return self.winning_pos

    def calculate_score(self, num_called):
        # sum of all unmarked numbers
        total = 0
        for y, row in enumerate(self.mark_rows):
            for x, val in enumerate(row):
                if val > self.winning_pos:
                    total += self.rows[y][x]
        return total * num_called


def get_numbers(drawn_numbers):
    return [int(x) for x in drawn_numbers.split(',')]


def solve(bingo_input):
    bingo_numbers = get_numbers(bingo_input[0])
    # create lookup table for bingo numbers with num as key and call position
    # as value
    bingo_numbers_dict = {key: val for (val, key) in enumerate(bingo_numbers)}

    this_board = []
    bingo_boards = []
    for row in bingo_input[2:]:
        if not row:
            bingo_boards.append(BingoBoard(this_board))
            this_board = []
        else:
            this_board.append(row)
    bingo_boards.append(BingoBoard(this_board))
    earliest = len(bingo_numbers)
    for board in bingo_boards:
        num = board.find_earliest_bingo(bingo_numbers_dict)
        if num < earliest:
            earliest = num
            bingo = board
    return bingo.calculate_score(bingo_numbers[bingo.winning_pos])


def solve_part_two(bingo_input):
    bingo_numbers = get_numbers(bingo_input[0])
    # create lookup table for bingo numbers with num as key and call position
    # as value
    bingo_numbers_dict = {key: val for (val, key) in enumerate(bingo_numbers)}

    this_board = []
    bingo_boards = []
    for row in bingo_input[2:]:
        if not row:
            bingo_boards.append(BingoBoard(this_board))
            this_board = []
        else:
            this_board.append(row)
    bingo_boards.append(BingoBoard(this_board))
    latest = 0
    for board in bingo_boards:
        num = board.find_earliest_bingo(bingo_numbers_dict)
        if num > latest:
            latest = num
            bingo = board
    return bingo.calculate_score(bingo_numbers[bingo.winning_pos])


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
