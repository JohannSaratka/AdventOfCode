'''
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey is
a ferry that goes directly to the tropical island where you can finally start
your vacation. As you reach the waiting area to board the ferry, you realize
you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the
waiting area, you're pretty sure you can predict the best place to sit. You
make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an
empty seat (L), or an occupied seat (#). For example, the initial seat layout
might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set of
rules. All decisions are based on the number of occupied seats adjacent to a
given seat (one of the eight positions immediately up, down, left, right, or
diagonal from the seat). The following rules are applied to every seat
simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the
seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also
occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes
occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats
become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further
applications of these rules cause no seats to change state! Once people stop
moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no
seats change state. How many seats end up occupied?

--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just
care about adjacent seats - they care about the first seat they can see in each
of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider
the first seat in each of those eight directions. For example, the empty seat
below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any
of the occupied ones:

.............
.L.L.#.#.#.#.
.............

The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or
more visible occupied seats for an occupied seat to become empty (rather than
four or more from the previous rules). The other rules still apply: empty seats
that see no occupied seats become occupied, seats matching no rule don't
change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area
to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches
equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming
empty, once equilibrium is reached, how many seats end up occupied?

Your puzzle answer was 2059.
'''

import unittest
from pylint.exceptions import InvalidArgsError


class Test(unittest.TestCase):
    def test_adapters(self):
        seat_layout = [
            "L.LL.LL.LL",
            "LLLLLLL.LL",
            "L.L.L..L..",
            "LLLL.LL.LL",
            "L.LL.LL.LL",
            "L.LLLLL.LL",
            "..L.L.....",
            "LLLLLLLLLL",
            "L.LLLLLL.L",
            "L.LLLLL.LL"]
        self.assertEqual(solve(seat_layout), 37)

    def test_visible_seats(self):
        seat_layout = [
            ".......L.",
            "...L.....",
            ".L.......",
            ".........",
            "..LL....L",
            "....L....",
            ".........",
            "L........",
            "...L....."]
        grid = Grid(seat_layout, 'visible')
        seat = grid.get_seat(3, 4)
        self.assertEqual(
            sum([1 for adjacent in seat.adjacent_seats if adjacent.active]),
            8)

    def test_visible_seats_and_higher_tolerance(self):
        seat_layout = [
            "L.LL.LL.LL",
            "LLLLLLL.LL",
            "L.L.L..L..",
            "LLLL.LL.LL",
            "L.LL.LL.LL",
            "L.LLLLL.LL",
            "..L.L.....",
            "LLLLLLLLLL",
            "L.LLLLLL.L",
            "L.LLLLL.LL"]
        self.assertEqual(solve_part_two(seat_layout), 26)


class Seat():
    def __init__(self, active, tolerance):
        self.active = active
        self.adjacent_seats = list()
        self.occupied = False
        self.next_state = False
        self.changed = False
        self.tolerance = tolerance

    def __str__(self):
        return "." if not self.active else 'L' if not self.occupied else '#'

    def connect(self, other):
        if not self.active:
            return
        if other is not None:
            self.adjacent_seats.append(other)

    def apply_rule(self):
        if not self.active:
            return
        neighbors = [s.occupied for s in self.adjacent_seats]
        if not self.occupied and not any(neighbors):
            self.next_state = True
            self.changed = True
        elif self.occupied and sum(neighbors) >= self.tolerance:
            self.next_state = False
            self.changed = True
        else:
            self.next_state = self.occupied
            self.changed = False

    def update(self):
        self.occupied = self.next_state


class Grid():
    def __init__(self, layout, mode='adjacent', tolerance=4):
        self.layout = [[None for col in row] for row in layout]
        self.length_y = len(layout)
        self.length_x = len(layout[0])

        for y, row in enumerate(layout):
            for x, seat in enumerate(row):
                self.layout[y][x] = Seat(seat == 'L', tolerance)
        if mode == 'adjacent':
            for y, row in enumerate(self.layout):
                for x, seat in enumerate(row):
                    seat.connect(self.get_seat(x - 1, y - 1))
                    seat.connect(self.get_seat(x, y - 1))
                    seat.connect(self.get_seat(x + 1, y - 1))
                    seat.connect(self.get_seat(x - 1, y))
                    seat.connect(self.get_seat(x + 1, y))
                    seat.connect(self.get_seat(x - 1, y + 1))
                    seat.connect(self.get_seat(x, y + 1))
                    seat.connect(self.get_seat(x + 1, y + 1))
        elif mode == 'visible':
            for y, row in enumerate(self.layout):
                for x, seat in enumerate(row):
                    seat.connect(self.get_active_seat(x, y, -1, -1))
                    seat.connect(self.get_active_seat(x, y, 0, -1))
                    seat.connect(self.get_active_seat(x, y, +1, -1))
                    seat.connect(self.get_active_seat(x, y, -1, 0))
                    seat.connect(self.get_active_seat(x, y, +1, 0))
                    seat.connect(self.get_active_seat(x, y, -1, +1))
                    seat.connect(self.get_active_seat(x, y, 0, +1))
                    seat.connect(self.get_active_seat(x, y, +1, +1))
        else:
            raise InvalidArgsError()

    def __str__(self):
        out = ""
        for row in self.layout:
            for seat in row:
                out += str(seat)
            out += '\n'
        return out

    def get_seat(self, x, y):
        if x < 0 or y < 0 or x >= self.length_x or y >= self.length_y:
            return None
        return self.layout[y][x]

    def get_active_seat(self, pos_x, pos_y, dir_x, dir_y):
        x = pos_x + dir_x
        y = pos_y + dir_y
        next_pos = self.get_seat(x, y)
        while next_pos:
            if next_pos.active:
                break
            x += dir_x
            y += dir_y
            next_pos = self.get_seat(x, y)
        return next_pos

    def has_changed(self):
        for row in self.layout:
            for seat in row:
                if seat.changed:
                    return True
        return False

    def next_round(self):
        for row in self.layout:
            for seat in row:
                seat.apply_rule()
        for row in self.layout:
            for seat in row:
                seat.update()

    def count_occupied(self):
        return sum([s.occupied for row in self.layout for s in row])


def solve(seat_layout):
    this_grid = Grid(seat_layout)
    # first round outside of loop because nothing changed yet
    this_grid.next_round()
    while this_grid.has_changed():
        this_grid.next_round()

    return this_grid.count_occupied()


def solve_part_two(seat_layout):
    this_grid = Grid(seat_layout, 'visible', 5)
    # first round outside of loop because nothing changed yet
    this_grid.next_round()
    while this_grid.has_changed():
        this_grid.next_round()

    return this_grid.count_occupied()


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
