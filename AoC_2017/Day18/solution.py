'''
Created on 01.12.2017

--- Day 18: Duet ---

It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that can each hold a single integer. You suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a number. The value of a register is the integer it contains; the value of a number is that number.

After each jump instruction, the program continues with the instruction to which the jump jumped. After any other instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a value of 4.
    Then, a sound with frequency 4 (the value of a) is played.
    After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
    Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump, which jumps again to the rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound played is 4.

What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv instruction is executed with a non-zero value?
--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

    snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive them. Each program has its own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock. When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0 might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send a value?

'''
import unittest

class Test(unittest.TestCase):
    
    def testPartOne(self):
        self.assertEqual(solve('set a 1\nadd a 2\nmul a a\nmod a 5\nsnd a\nset a 0\nrcv a\njgz a -1\nset a 1\njgz a -2'), 4)
    def testPartTwo(self):
        self.assertEqual(solvePartTwo('snd 1\nsnd 2\nsnd p\nrcv a\nrcv b\nrcv c\nrcv d'), 3)

def solve(input_list):
    instr_list = input_list.split('\n')
    pc=0
    register = dict()
    last_sound_played = 0
    while True:
        # decode
        instr = instr_list[pc].split()
        if not instr[1].isdigit():
            register.setdefault(instr[1],0)
        if instr[0] == 'snd':            
            last_sound_played = register[instr[1]]
        elif instr[0] == 'set':
            try:
                register[instr[1]] = int(instr[2])
            except ValueError:
                register[instr[1]] = register[instr[2]]
        elif instr[0] == 'add':
            try:
                register[instr[1]] += int(instr[2])
            except ValueError:
                register[instr[1]] += register[instr[2]]
        elif instr[0] == 'mul':
            try:
                register[instr[1]] *= int(instr[2])
            except ValueError:
                register[instr[1]] *= register[instr[2]]
        elif instr[0] == 'mod':
            try:
                register[instr[1]] %= int(instr[2])
            except ValueError:
                register[instr[1]] %= register[instr[2]]
        elif instr[0] == 'rcv':
            if register[instr[1]]!= 0:
                return last_sound_played
        elif instr[0] == 'jgz':
            try:
                if register[instr[1]] > 0:
                    try:
                        pc += int(instr[2])
                    except ValueError:
                        pc += register[instr[2]]
                    continue
            except KeyError:
                if int(instr) > 0:
                    pc += int(instr[2])
                    continue
        pc += 1
    
def solvePartTwo(input_list):
    d0 = Duett(input_list.split('\n'),0)
    d1 = Duett(input_list.split('\n'),1)
    d0.setPartner(d1)
    d1.setPartner(d0)
    while d0.running or d1.running:
        d0.run()
        d1.run()
    return d1.snd_count

class Duett(object):
    def __init__(self,instr_list,prog_id):
        self.instr_list = instr_list
        self.pc = 0
        self.register = {'p': prog_id}
        self.queue = list()
        self.running = True
        self.snd_count = 0
        self.instr_dict = {'snd': self.snd,
                          'set': self.set,
                          'add': self.add,
                          'mul': self.mul,
                          'mod': self.mod,
                          'rcv': self.rcv,
                          'jgz': self.jgz,
                          }
        
    def setPartner(self,other):
        self.other = other
        
    def send(self,value):
        self.queue.append(value)
        self.running = True
             
    def run(self):
        while self.running:
            instr = self.instr_list[self.pc].split()
            if not instr[1].isdigit():
                self.register.setdefault(instr[1],0)
            self.instr_dict[instr[0]](instr)
            
            self.pc += 1

    def snd(self,instr):
        self.other.send(self.register[instr[1]])
        self.snd_count += 1
        
    def set(self,instr):
        if instr[2].isdigit():
            self.register[instr[1]] = int(instr[2])
        else:
            self.register[instr[1]] = self.register[instr[2]]
            
    def add(self,instr):                
        if instr[2].lstrip('-').isdigit():
            self.register[instr[1]] += int(instr[2])
        else:
            self.register[instr[1]] += self.register[instr[2]]
    
    def mul(self,instr):
            self.register[instr[1]] *= int(instr[2])
    
    def mod(self,instr):
        if instr[2].isdigit():
            self.register[instr[1]] %= int(instr[2])
        else:
            self.register[instr[1]] %= self.register[instr[2]]
    
    def rcv(self,instr):
        try:
            self.register[instr[1]] = self.queue.pop(0)
        except IndexError:
            self.running = False
            self.pc -= 1 # remove auto increment
    
    def jgz(self,instr):
        try:
            if self.register[instr[1]] > 0:
                try:
                    self.pc += int(instr[2])
                except ValueError:
                    self.pc += self.register[instr[2]]
                self.pc -= 1 # remove auto increment
        except KeyError:
            if int(instr[1]) > 0:
                self.pc += int(instr[2])
                
                self.pc -= 1 # remove auto increment
            
enableUnitTest = False


if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:           
            puzzleInput = inFile.read().rstrip()
            print solve(puzzleInput)
            print solvePartTwo(puzzleInput)