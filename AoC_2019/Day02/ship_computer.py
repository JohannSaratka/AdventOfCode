'''
Created on 06.12.2019

@author: johann
'''
import unittest

class Test(unittest.TestCase):
    def assertProgramExecution(self,initial_memory, expected_memory):
        ship = ShipComputer(initial_memory)
        self.assertEqual(ship.run(), 
                         expected_memory)
    def testProg1(self):
        self.assertProgramExecution([1,9,10,3,2,3,11,0,99,30,40,50], 
                         [3500,9,10,70,2,3,11,0,99,30,40,50])
        
    def testProg2(self):
        self.assertProgramExecution([1,0,0,0,99], [2,0,0,0,99])
        
    def testProg3(self):
        self.assertProgramExecution([2,3,0,3,99], [2,3,0,6,99])
        
    def testProg4(self):
        self.assertProgramExecution([2,4,4,5,99,0 ], [2,4,4,5,99,9801])
        
    def testProg5(self):
        self.assertProgramExecution([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
     
class ShipComputer():
    def __init__(self, program):
        self.pc = 0
        self.memory = program
        
    def run(self):
        while(True):
            # instruction fetch
            instr_cache = self.memory[self.pc]
            # decode + execute + store
            if instr_cache == 1:
                # add uses indirect addressing, @c = @a + @b 
                param_a , param_b, param_c = self.memory[self.pc+1:self.pc+4]
                self.memory[param_c] = self.memory[param_a] + self.memory[param_b]
                instr_size = 4
                
            elif instr_cache == 2:
                # mul @c = @a * @b 
                param_a , param_b, param_c = self.memory[self.pc+1:self.pc+4]
                self.memory[param_c] = self.memory[param_a] * self.memory[param_b]
                instr_size = 4
                
            elif instr_cache == 99:
                break
            self.pc += instr_size
        return self.memory

def intCodeToList(intCodeProg):
    return [int(x) for x in intCodeProg[0].split(',')]

if __name__ == '__main__':
    pass