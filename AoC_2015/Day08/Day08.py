r'''
--- Day 8: Matchsticks ---

Space on the sleigh is limited this year, and so Santa will be bringing his
list as a digital copy. He needs to know how much space it will take up when
stored.

It is common in many programming languages to provide a way to escape special
characters in strings. For example, C, JavaScript, Perl, Python, and even PHP
handle special characters in very similar ways.

However, it is important to realize the difference between the number of
characters in the code representation of the string literal and the number of
characters in the in-memory string itself.

For example:

    "" is 2 characters of code (the two double quotes), but the string contains
zero characters.
    "abc" is 5 characters of code, but 3 characters in the string data.
    "aaa\"aaa" is 10 characters of code, but the string itself contains six "a"
characters and a single, escaped quote character, for a total of 7 characters
in the string data.
    "\x27" is 6 characters of code, but the string itself contains just one -
an apostrophe ('), escaped using hexadecimal notation.

Santa's list is a file that contains many double-quoted string literals, one on
each line. The only escape sequences used are \\ (which represents a single
backslash), \" (which represents a lone double-quote character), and \x plus
two hexadecimal characters (which represents a single character with that ASCII
code).

Disregarding the whitespace in the file, what is the number of characters of
code for string literals minus the number of characters in memory for the
values of the strings in total for the entire file?

For example, given the four strings above, the total number of characters of
string code (2 + 5 + 10 + 6 = 23) minus the total number of characters in
memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.

--- Part Two ---

Now, let's go the other way. In addition to finding the number of characters of
code, you should now encode each code representation as a new string and find
the number of characters of the new encoded representation, including the
surrounding double quotes.

For example:

    "" encodes to "\"\"", an increase from 2 characters to 6.
    "abc" encodes to "\"abc\"", an increase from 5 characters to 9.
    "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to
16.
    "\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11.

Your task is to find the total number of characters to represent the newly
encoded strings minus the number of characters of code in each original string
literal. For example, for the strings above, the total encoded length (6 + 9 +
16 + 11 = 42) minus the characters in the original code representation (23,
just like in the first part of this puzzle) is 42 - 23 = 19.
'''

import unittest


class Test(unittest.TestCase):
    def test_get_size_difference_no_chars(self):
        self.assertEqual(get_size_difference('""'), 2)

    def test_get_size_difference_string(self):
        self.assertEqual(get_size_difference('"abc"'), 2)

    def test_get_size_difference_escape_double_quote(self):
        self.assertEqual(get_size_difference('"aaa\\"aaa"'), 3)

    def test_get_size_difference_escape_backslash(self):
        self.assertEqual(get_size_difference('"aaa\\\\aaa"'), 3)

    def test_get_size_difference_escape_ascii(self):
        self.assertEqual(get_size_difference('"\\x27"'), 5)
        self.assertEqual(get_size_difference('"gzkxqrdq\\\\uko\\"mrtst"'), 4)

    def test_new_encode_two_double_quotes(self):
        self.assertEqual(new_encode('""'), 4)

    def test_new_encode_string(self):
        self.assertEqual(new_encode('"abc"'), 4)

    def test_new_encode_escape_quote(self):
        self.assertEqual(new_encode('"aaa\\"aaa"'), 6)

    def test_new_encode_escape_ascii(self):
        self.assertEqual(new_encode('"\\x27"'), 5)


def get_size_difference(strng):
    size_string = 0
    size_code = len(strng)
    i = 1  # always ignore leading and trailing quotes
    while i < size_code - 1:
        if strng[i] is '\\':
            if strng[i + 1] is 'x':
                i += 4
            else:
                i += 2
        else:
            i += 1
        size_string += 1
    return size_code - size_string


def new_encode(strng):
    new_strng = ""
    for c in strng:
        if c is '"':
            new_strng += '\\"'
        elif c is '\\':
            new_strng += '\\\\'
        else:
            new_strng += c
    return len(new_strng) + 2 - len(strng)


def solve(santas_list):
    total_part1 = 0
    total_part2 = 0
    for n, element in enumerate(santas_list):
        total_part1 += get_size_difference(element)
        total_part2 += new_encode(element)
    return total_part1, total_part2


if __name__ == "__main__":
    with open('Day08Data.txt', 'r')as f:
        puzzleInput = f.read().splitlines()
        print("Solution: {}".format(solve(puzzleInput)))
