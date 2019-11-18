'''
Created on 01.12.2017

--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?
--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes. Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?

'''
import unittest

# class Test(unittest.TestCase):
#     
#     def testPartOne(self):
#         self.assertEqual(solve('set a 1\nadd a 2\nmul a a\nmod a 5\nsnd a\nset a 0\nrcv a\njgz a -1\nset a 1\njgz a -2'), 4)
#     def testPartTwo(self):
#         self.assertEqual(solvePartTwo('snd 1\nsnd 2\nsnd p\nrcv a\nrcv b\nrcv c\nrcv d'), 3)

def solve(input_list,value_a=0):
    instr_list = input_list.split('\n')
    pc=0
    register = dict((x,0) for x in 'abcdefgh')
    register['a'] = value_a
    mul_count = 0
    while True:
        # decode
        try:
            instr = instr_list[pc].split()
        except IndexError:
            if value_a == 0:
                return mul_count
            else:
                return register['h']

        if instr[0] == 'set':
            if instr[2].lstrip('-').isdigit():
                register[instr[1]] = int(instr[2])
            else:
                register[instr[1]] = register[instr[2]]

        elif instr[0] == 'sub':
            if instr[2].lstrip('-').isdigit():
                register[instr[1]] -= int(instr[2])
            else:
                register[instr[1]] -= register[instr[2]]
                
        elif instr[0] == 'mul':
            mul_count+=1
            if instr[2].lstrip('-').isdigit():
                register[instr[1]] *= int(instr[2])
            else:
                register[instr[1]] *= register[instr[2]]

        elif instr[0] == 'jnz':            
            if instr[1].lstrip('-').isdigit():
                test_reg = int(instr[1])
            else:
                test_reg = register[instr[1]]
            if test_reg != 0:
                if instr[2].lstrip('-').isdigit():
                    pc += int(instr[2])
                else:
                    pc += register[instr[2]]
                continue

        pc += 1

def solvePartTwo():
    start_b=105700
    c=start_b+17000
    n=0
    h=0
    for b in xrange(start_b,c,17):
        n+=1
        for i in xrange(2,b):
            if (b % i) == 0:
#                 print(b,"is not a prime number")
#                 print(i,"times",b//i,"is",b)
                h+=1
                break
        else:
            print(b,"is a prime number")
        #f=1 #set f 1
        #set d 2
        #for d in xrange(2,b):
            #set e 2
            #for e in xrange(2,b):    
                #set g d
                # mul g e
                # sub g b
                #jnz g 2
                #if d*e==b:
                    #f=0 #set f 0
                    #print "%d, %d, %d" % (d,e,b)
                    #break
                #sub e -1
                #set g e
                #sub g b
                #jnz g -8
            #if f==0:
                #break   
            #sub d -1
            #set g d
            #sub g b
            #jnz g -13

        #if f==0: #jnz f 2
            #h+=1 #sub h -1
        #set g b
        #sub g c
        #jnz g 2
        #jnz 1 3
        #sub b -17
        #jnz 1 -23
    return n,h
  
          
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:           
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput)
            print solvePartTwo()