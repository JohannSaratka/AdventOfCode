'''
Created on 01.12.2017

--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the 
CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves 
that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

'''
import unittest
import re
from collections import namedtuple
Instruction = namedtuple('Instruction', ['reg_to_mod','do_inc','inc_amount','cond_reg','condition','cond_value'])

class Test(unittest.TestCase):
    def testOne(self):
        with open("test_input.txt",'r') as testFile:
            self.assertEqual(solve(testFile.read().rstrip()), 1)

        
def solve(input_list):
    re_instruction = re.compile(r'(\w+)\s(dec|inc)\s(-?\d+)\sif\s(\w+)\s([<>!=]+)\s(-?\d+)')
    register_dict=dict()
    all_time_max = 0
    for line in input_list.split("\n"):
        instr = Instruction(*(re_instruction.findall(line))[0])
        register_dict.setdefault(instr.cond_reg,0)
        register_dict.setdefault(instr.reg_to_mod,0)
        
        val1 = register_dict[instr.cond_reg]
        val2 = int(instr.cond_value)
        if ((instr.condition == '==' and val1 == val2) or
            (instr.condition == '>=' and val1 >= val2) or
            (instr.condition == '>' and val1 > val2) or
            (instr.condition == '<' and val1 < val2) or
            (instr.condition == '<=' and val1 <= val2) or
            (instr.condition == '!=' and val1 != val2)):
            register_dict[instr.reg_to_mod] += ((1) if instr.do_inc == 'inc' else -1) * int(instr.inc_amount)
        all_time_max = max(all_time_max,max(register_dict.values()))
    return max(register_dict.values()), all_time_max

            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput)
    