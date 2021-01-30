'''
--- Day 11: Corporate Policy ---

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has
devised a method of coming up with a password based on the previous one.
Corporate policy dictates that passwords must be exactly eight lowercase
letters (for security reasons), so he finds his new password by incrementing
his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on.
Increase the rightmost letter one step; if it was z, it wraps around to a, and
repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has
imposed some additional password requirements:

    Passwords must include one increasing straight of at least three letters,
like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't
count.
    Passwords may not contain the letters i, o, or l, as these letters can be
mistaken for other characters and are therefore confusing.
    Passwords must contain at least two different, non-overlapping pairs of
letters, like aa, bb, or zz.

For example:

    hijklmmn meets the first requirement (because it contains the straight hij)
but fails the second requirement requirement (because it contains i and l).
    abbceffg meets the third requirement (because it repeats bb and ff) but
fails the first requirement.
    abbcegjk fails the third requirement, because it only has one double letter
(bb).
    The next password after abcdefgh is abcdffaa.
    The next password after ghijklmn is ghjaabcc, because you eventually skip
all the passwords that start with ghi..., since i is not allowed.

Given Santa's current password (your puzzle input), what should his next
password be?

'''

import unittest
import re


class Test(unittest.TestCase):
    def check_inc(self, start_pwd, expected_inc_pwd):
        pwd = Password(start_pwd)
        pwd.inc()
        self.assertEqual(str(pwd), expected_inc_pwd)

    def test_all_positions_increment(self):
        self.check_inc("aaaaaaaa", "aaaaaaab")
        self.check_inc("aaaaaabz", "aaaaaaca")
        self.check_inc("aaaaaczz", "aaaaadaa")
        self.check_inc("aaaadzzz", "aaaaeaaa")
        self.check_inc("aaaezzzz", "aaafaaaa")
        self.check_inc("aafzzzzz", "aagaaaaa")
        self.check_inc("agzzzzzz", "ahaaaaaa")
        self.check_inc("jzzzzzzz", "kaaaaaaa")

    def test_skip_iol(self):
        self.check_inc("aaaaaaah", "aaaaaaaj")
        self.check_inc("aaaaaaak", "aaaaaaam")
        self.check_inc("aaaaaaan", "aaaaaaap")

    def test_has_three_inc_straight(self):
        self.assertTrue(Password("hjjkmpqr").has_three_inc_straight())
        self.assertFalse(Password("abbceffg").has_three_inc_straight())
        self.assertFalse(Password("abbcegjk").has_three_inc_straight())
        self.assertFalse(Password("abbzabjk").has_three_inc_straight())

    def test_has_two_valid_pairs(self):
        self.assertTrue(Password("abbceffg").has_two_valid_pairs())
        self.assertFalse(
            Password("abbcegjk").has_two_valid_pairs())  # only one
        self.assertFalse(
            Password("aaabbcda").has_two_valid_pairs())  # overlapping
        self.assertTrue(Password("aaabbccd").has_two_valid_pairs())
        self.assertTrue(
            Password("aabbccde").has_two_valid_pairs())  # more than two
        # two different two of the same
        self.assertTrue(
            Password("aabbaade").has_two_valid_pairs())
        # not different and overlap
        self.assertFalse(
            Password("aaaaghde").has_two_valid_pairs())
        self.assertFalse(
            Password("aagaahde").has_two_valid_pairs())  # not different

        self.assertFalse(Password("ababcgde").has_two_valid_pairs())

    def test_get_next_password(self):
        self.assertEqual(solve("abcdefgh"), "abcdffaa")
        self.assertEqual(solve("ghijklmn"), "ghjaabcc")


class Letter():
    def __init__(self, c):
        self.c = c
        self.did_wrap = False

    def __str__(self):
        return self.c

    def __repr__(self):
        return f"Letter {str(self)}"

    def __iadd__(self, other):
        if isinstance(other, int):
            if self.c == 'z':
                self.c = 'a'
                self.did_wrap = True
            else:
                self.c = chr(ord(self.c) + other)
                self.did_wrap = False
            return self
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):
            new_c = chr(ord(self.c) - other)
            return Letter(new_c)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Letter):
            return self.c == other.c
        return False

    def is_invalid(self):
        return self.c in ['i', 'l', 'o']

    def inc(self):
        self += 1
        if self.is_invalid():
            self += 1


class Password():
    def __init__(self, previous):
        self.value = [Letter(c) for c in previous]
        # handle case where previous password includes i, o or l
        for i, letter in enumerate(self.value):
            if letter.is_invalid():
                letter.inc()
                for other in self.value[i + 1:]:
                    other.c = 'a'
                break

    def inc(self):
        i = 7
        self.value[i].inc()
        while self.value[i].did_wrap:
            i -= 1  # wrap around in last position is unlikely
            self.value[i].inc()

    def has_three_inc_straight(self):
        threes = [self.value[i:i + 3] for i, _ in enumerate(self.value[:-2])]
        for block in threes:
            if block[0] == (block[1] - 1) == (block[2] - 2):
                return True
        return False

    def find_pairs(self):
        # match either A or B if A matches B is ignored
        # A: any letter repeated more than 2 times
        # B: any letter repeated exactly twice
        pairs = re.findall(r'([a-z])\1{2,}|([a-z])\2', str(self))
        # only use B
        return [y + y for _, y in pairs if y]

    def has_two_valid_pairs(self):
        pairs = set(self.find_pairs())
        if len(pairs) < 2:
            return False
        return True

    def __str__(self):
        return "".join(str(l) for l in self.value)


def solve(start):
    pwd = Password(start)
    pwd.inc()
    while((not pwd.has_three_inc_straight()) or
          (not pwd.has_two_valid_pairs())):
        pwd.inc()
    return str(pwd)


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzle_input = inFile.read().splitlines()
        solution_one = solve(puzzle_input[0])
        print(f"Solution Part 1: {solution_one}")
        print(f"Solution Part 2: {solve(solution_one)}")
