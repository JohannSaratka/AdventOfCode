'''
--- Day 16: Ticket Translation ---
As you're walking to yet another connecting flight, you realize that one of
the legs of your re-routed trip coming up is on a high-speed train. However,
the train ticket you were given is in a language you don't understand. You
should probably figure out what it says before you get to the train station
after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can,
however, read the numbers, and so you figure out the fields these tickets
must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the
numbers on other nearby tickets for the same train service (via the airport
security cameras) together into a single document you can reference (your
puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on
the ticket and the valid ranges of values for each field. For example, a rule
like class: 1-3 or 5-7 means that one of the fields in every ticket is named
class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3
and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The
values are the numbers on the ticket in the order they appear; every ticket
has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might
be represented as 101,102,103,104,301,302,303,401,402,403; of course, the
actual train tickets you're looking at are much more complicated. In any case,
you've extracted just the numbers in such a way that the first number is
always the same specific field, the second number is always a different
specific field, and so on - you just don't know what each position actually
means!

Start by determining which tickets are completely invalid; these are tickets
that contain values which aren't valid for any field. Ignore your ticket for
now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify
invalid nearby tickets by considering only whether tickets contain values that
are not valid for any field. In this example, the values on the first nearby
ticket are all valid for at least one field. This is not true of the other
three nearby tickets: the values 4, 55, and 12 are are not valid for any
field. Adding together all of the invalid values produces your ticket scanning
error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket
scanning error rate?

--- Part Two ---
Now that you've identified which tickets contain invalid values, discard those
tickets entirely. Use the remaining valid tickets to determine which field is
which.

Using the valid ranges for each field, determine what order the fields appear
on the tickets. The order is consistent between all tickets: if seat is the
third field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
Based on the nearby tickets in the above example, the first position must be
row, the second position must be class, and the third position must be seat;
you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket
that start with the word departure. What do you get if you multiply those six
values together?
'''

import unittest
import re


class Test(unittest.TestCase):
    def test_field_order(self):
        notes = (
            "class: 0-1 or 4-19\n"
            "row: 0-5 or 8-19\n"
            "seat: 0-13 or 16-19\n"
            "\n"
            "your ticket:\n"
            "11,12,13\n"
            "\n"
            "nearby tickets:\n"
            "3,9,18\n"
            "15,1,5\n"
            "5,14,9")
        fields = get_field_list(notes)
        self.assertEqual([f.name for f in fields], ["row", "class", "seat"])

    def test_ticket_error_rate(self):
        notes = (
            "class: 1-3 or 5-7\n"
            "row: 6-11 or 33-44\n"
            "seat: 13-40 or 45-50\n"
            "\n"
            "your ticket:\n"
            "7,1,14\n"
            "\n"
            "nearby tickets:\n"
            "7,3,47\n"
            "40,4,50\n"
            "55,2,20\n"
            "38,6,12")
        self.assertEqual(solve(notes), 71)


class Field():
    def __init__(self, name, a, b, c, d):
        self.name = name
        self.range1 = (int(a), int(b))
        self.range2 = (int(c), int(d))
        self.values = []
        self.values.extend(range(self.range1[0], self.range1[1] + 1))
        self.values.extend(range(self.range2[0], self.range2[1] + 1))
        self.position = []

    def __repr__(self):
        return "{}: {}-{} or {}-{}".format(self.name,
                                           self.range1[0], self.range1[1],
                                           self.range2[0], self.range2[1])

    def get_ranges(self):
        return self.values

    def value_in_range(self, value):
        return value in self.values

    def reduce_positions(self, filter_list):
        self.position = [x for x in self.position if x not in filter_list]


def solve(notes):
    prog = re.compile(r'(\w+ *\w*): (\d+)-(\d+) or (\d+)-(\d+)')
    fields = []
    ticket_rules = prog.findall(notes)
    for rule in ticket_rules:
        f = Field(*rule)
        fields.append(f)
    all_ranges = []
    for field in fields:
        all_ranges.extend(field.get_ranges())

    valid_range = set(all_ranges)
    token = "nearby tickets:\n"
    other_tickets_id = notes.index(token)
    other_tickets = notes[other_tickets_id + len(token):].splitlines()
    error_rate = 0
    for ticket in other_tickets:
        for value in map(int, ticket.split(',')):
            if value not in valid_range:
                error_rate += value
    return error_rate


def solve_part_two(notes):
    fields = get_field_list(notes)
    is_ticket = False
    ticket = ""
    for line in notes.splitlines():
        if "your" in line:
            is_ticket = True
        elif is_ticket:
            ticket = line
            break
    ticket = list(map(int, ticket.split(',')))
    total = 1
    # finding values for fields starting with departure
    # multiply these values
    for field in fields:
        if "departure" in field.name:
            total *= ticket[field.position[0]]
    return total


def get_field_list(notes):
    prog = re.compile(r'(\w+ *\w*): (\d+)-(\d+) or (\d+)-(\d+)')
    fields = []
    # create fields
    ticket_rules = prog.findall(notes)
    for rule in ticket_rules:
        field = Field(*rule)
        fields.append(field)

    # find valid tickets
    all_ranges = []
    for field in fields:
        all_ranges.extend(field.get_ranges())

    valid_range = set(all_ranges)
    token = "nearby tickets:\n"
    other_tickets_id = notes.index(token)
    other_tickets = notes[other_tickets_id + len(token):].splitlines()
    valid_tickets = []
    for ticket in other_tickets:
        for value in map(int, ticket.split(',')):
            if value not in valid_range:
                break
        else:
            valid_tickets.append(map(int, ticket.split(',')))

    # transpose to iterate each position
    valid_tickets_transpose = [list(x) for x in zip(*valid_tickets)]
    for field in fields:
        for i, row in enumerate(valid_tickets_transpose):
            for value in row:
                if not field.value_in_range(value):
                    break
            else:
                # all values are within range
                field.position.append(i)
    # sort by length of possible positions
    # a field with only one possible position will be first then two then three
    # Since the first field is only possible in a single position this position
    # can be removed from all following fields.
    # This will reduce the following fields and can be repeated until all
    # fields only have a single position available.
    fields.sort(key=lambda f: len(f.position))
    filter_list = []
    for field in fields:
        field.reduce_positions(filter_list)
        filter_list.extend(field.position)

    fields.sort(key=lambda f: f.position)

    return fields


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
