'''
--- Day 4: Passport Processing ---

You arrive at the airport only to realize that you grabbed your North Pole
Credentials instead of your passport. While these documents are extremely
similar, North Pole Credentials aren't issued by a country and therefore
aren't actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line
has formed for the automatic passport scanners, and the delay could upset your
travel itinerary.

Due to some questionable network security, you realize you might be able to
solve both of these problems at the same time.

The automatic passport scanners are slow because they're having trouble
detecting which passports have all required fields. The expected fields are as
follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is
represented as a sequence of key:value pairs separated by spaces or newlines.
Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

The first passport is valid - all eight fields are present. The second passport
is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks
like data from North Pole Credentials, not a passport at all! Surely, nobody
would mind if you made the system temporarily ignore missing cid fields. Treat
this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but
missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid
passports.

Count the number of valid passports - those that have all required fields.
Treat cid as optional. In your batch file, how many passports are valid?

'''

import unittest
import string

class Test(unittest.TestCase):

    def test_simple_count(self):
        batch_file = [
            "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
            "byr:1937 iyr:2017 cid:147 hgt:183cm",
            "",
            "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
            "hcl:#cfa07d byr:1929",
            "",
            "hcl:#ae17e1 iyr:2013",
            "eyr:2024",
            "ecl:brn pid:760753108 byr:1931",
            "hgt:179cm",
            "",
            "hcl:#cfa07d eyr:2025 pid:166559648",
            "iyr:2011 ecl:brn hgt:59in"]

        self.assertEqual(solve(batch_file), 2)

    def test_complex_count_no_valid(self):
        batch_file = [
            "eyr:1972 cid:100",
            "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
            "",
            "iyr:2019",
            "hcl:#602927 eyr:1967 hgt:170cm",
            "ecl:grn pid:012533040 byr:1946",
            "",
            "hcl:dab227 iyr:2012",
            "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
            "",
            "hgt:59cm ecl:zzz",
            "eyr:2038 hcl:74454a iyr:2023",
            "pid:3556412378 byr:2007"]

        self.assertEqual(solve_part_two(batch_file), 0)

    def test_complex_count_all_valid(self):
        batch_file = [
            "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
            "hcl:#623a2f",
            "",
            "eyr:2029 ecl:blu cid:129 byr:1989",
            "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
            "",
            "hcl:#888785",
            "hgt:164cm byr:2001 iyr:2015 cid:88",
            "pid:545766238 ecl:hzl",
            "eyr:2022",
            "",
            "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"]

        self.assertEqual(solve_part_two(batch_file), 4)


def byr_check(value):
    return 1920 <= int(value) <= 2002


def iyr_check(value):
    return 2010 <= int(value) <= 2020


def eyr_check(value):
    return 2020 <= int(value) <= 2030


def hgt_check(value):
    if 'cm' in value:
        return 150 <= int(value[:-2]) <= 193
    elif 'in' in value:
        return 59 <= int(value[:-2]) <= 76
    else:
        return False


def hcl_check(value):
    if value[0] is not '#':
        return False
    return all(char in string.hexdigits for char in value[1:])


def ecl_check(value):
    possible_ecl = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    return value in possible_ecl


def pid_check(value):
    return value.isdigit() and len(value) == 9


def solve(batch_file):
    passport = dict()
    passports = list()
    for line in batch_file:
        if len(line) == 0:
            passports.append(passport.copy())
            passport = dict()
            continue
        for pair in line.split(' '):
            key, value = pair.split(':')
            passport[key] = value
    # add last passport
    passports.append(passport.copy())
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    num_valid = 0

    for passport in passports:
        if required_fields.issubset(passport.keys()):
            num_valid += 1
    return num_valid


def solve_part_two(batch_file):
    passport = dict()
    passports = list()
    for line in batch_file:
        if len(line) == 0:
            passports.append(passport.copy())
            passport = dict()
            continue
        for pair in line.split(' '):
            key, value = pair.split(':')
            passport[key] = value
    # add last passport
    passports.append(passport.copy())
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    num_valid = 0

    for passport in passports:
        if required_fields.issubset(passport.keys()):
            valid = (byr_check(passport['byr'])
                     and iyr_check(passport['iyr'])
                     and eyr_check(passport['eyr'])
                     and hgt_check(passport['hgt'])
                     and hcl_check(passport['hcl'])
                     and ecl_check(passport['ecl'])
                     and pid_check(passport['pid']))
            num_valid += 1 if valid else 0
    return num_valid


if __name__ == "__main__":
    with open("input.txt", 'r') as inFile:
        puzzleInput = inFile.read().splitlines()
        print("Solution Part 1: {}".format(solve(puzzleInput)))
        print("Solution Part 2: {}".format(solve_part_two(puzzleInput)))
