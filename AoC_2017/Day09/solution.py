'''
Created on 01.12.2017

--- Day 9: Stream Processing ---

A large stream blocks your path. According to the locals, it's not safe to cross the stream at the moment because it's full of garbage. You look down at the stream; rather than water, you discover that it's a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The characters represent groups - sequences that begin with { and end with }. Within a group, there are zero or more other things, separated by commas: either another group or garbage. Since groups can contain other groups, a } only closes the most-recently-opened unclosed group - that is, they are nestable. Your puzzle input represents a single, large group which itself contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with < and ends with >. Between those angle brackets, almost any character can appear, including { and }. Within garbage, < has no special meaning.

In a futile attempt to clean up the garbage, some program has canceled some of the characters within it using !: inside garbage, any character that comes after ! should be ignored, including <, >, and even another !.

You don't see any characters that deviate from these rules. Outside garbage, you only find well-formed groups, and garbage always terminates according to the rules above.

Here are some self-contained pieces of garbage:

    <>, empty garbage.
    <random characters>, garbage containing random characters.
    <<<<>, because the extra < are ignored.
    <{!>}>, because the first > is canceled.
    <!!>, because the second ! is canceled, allowing the > to terminate the garbage.
    <!!!>>, because the second ! and the first > are canceled.
    <{o"i!a,<{i<a>, which ends at the first >.

Here are some examples of whole streams and the number of groups they contain:

    {}, 1 group.
    {{{}}}, 3 groups.
    {{},{}}, also 3 groups.
    {{{},{},{{}}}}, 6 groups.
    {<{},{},{{}}>}, 1 group (which itself contains garbage).
    {<a>,<a>,<a>,<a>}, 1 group.
    {{<a>},{<a>},{<a>},{<a>}}, 5 groups.
    {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

Your goal is to find the total score for all groups in your input. Each group is assigned a score which is one more than the score of the group that immediately contains it. (The outermost group gets a score of 1.)

    {}, score of 1.
    {{{}}}, score of 1 + 2 + 3 = 6.
    {{},{}}, score of 1 + 2 + 2 = 5.
    {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
    {<a>,<a>,<a>,<a>}, score of 1.
    {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

What is the total score for all groups in your input?
--- Part Two ---

Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the garbage. The leading and trailing < and > don't count, nor do any canceled characters or the ! doing the canceling.

    <>, 0 characters.
    <random characters>, 17 characters.
    <<<<>, 3 characters.
    <{!>}>, 2 characters.
    <!!>, 0 characters.
    <!!!>>, 0 characters.
    <{o"i!a,<{i<a>, 10 characters.

How many non-canceled characters are within the garbage in your puzzle input?

'''
import unittest


class Test(unittest.TestCase):
    def assertDataList(self,fun_to_test,test_data):
        for data, expectation in test_data:
            actual = fun_to_test(data)
            self.assertEqual(actual, expectation,"Data: " + data + "\nExpected: " + str(expectation)+"\nActual: " + str(actual))
        
    def testGroups(self):
        test_data = [['{}',1],
                     ['{{{}}}',3],
                     ['{{},{}}',3],
                     ['{{{},{},{{}}}}',6],
                     ['{<{},{},{{}}>}',1],
                     ['{<a>,<a>,<a>,<a>}',1],
                     ['{{<a>},{<a>},{<a>},{<a>}}',5],
                     ['{{<!>},{<!>},{<!>},{<a>}}',2],
                     ]
        self.assertDataList(findGroups,test_data)
        
    def testGarbage(self):
        test_data = [['{<>}',1], 
                     ['{<random characters>}',1],
                     ['{<<<<>}',1],
                     ['{<{!>}>}',1],
                     ['{<!!>}',1],
                     ['{<!!!>>}',1],
                     ['{<{o"i!a,<{i<a>}',1],
                     ]
        self.assertDataList(findGroups,test_data)
        
    def testScoring(self):
        test_data = [['{}',1],
                     ['{{{}}}', 6],
                     ['{{},{}}', 5],
                     ['{{{},{},{{}}}}', 16],
                     ['{<a>,<a>,<a>,<a>}',1],
                     ['{{<ab>},{<ab>},{<ab>},{<ab>}}',9],
                     ['{{<!!>},{<!!>},{<!!>},{<!!>}}', 9],
                     ['{{<a!>},{<a!>},{<a!>},{<ab>}}',3],
                     ]
        self.assertDataList(getScore,test_data)
    def testCountRemovedGarbage(self):
        test_data = [['<>', 0 ],
                     ['<random characters>', 17 ],
                     ['<<<<>', 3 ],
                     ['<{!>}>', 2 ],
                     ['<!!>', 0 ],
                     ['<!!!>>', 0 ],
                     ['<{o"i!a,<{i<a>', 10 ],
                     ]
        self.assertDataList(getRemovedGarbage,test_data)
        
def findGroups(line):
    gc=GarbageCompactor()
    gc.run(line)
    return gc.num_of_groups

def getScore(line):
    gc = GarbageCompactor()
    gc.run(line)
    return gc.total_score

def getRemovedGarbage(line):
    gc = GarbageCompactor()
    gc.run(line)
    return gc.garbage_count

class GarbageCompactor(object):
    def __init__(self):
        self.open_groups = 0
        self.num_of_groups = 0
        self.open_garbage = False
        self.cancel_next = False
        self.total_score = 0
        self.garbage_count = 0
        
    def run(self,line):
        for c in line:
            self.next_char(c)
            
    def next_char(self,c):
        if self.cancel_next:
            self.cancel_next=False
            return
        
        if c=='!':
            self.cancel_next = True
            return
        
        if self.open_garbage:
            if c == '>':
                self.open_garbage = False
            else:
                self.garbage_count += 1  
            return
                
        if c == '{':
            self.open_groups += 1
            self.num_of_groups +=1
            self.total_score+=self.open_groups
        elif c == '}':
            self.open_groups -= 1
        elif c == '<':
            self.open_garbage = True
     
def solve(input_list):
    return getScore(input_list)

def solvePartTwo(input_list):
    return getRemovedGarbage(input_list)
                
            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput),
            print solvePartTwo(puzzleInput)
    