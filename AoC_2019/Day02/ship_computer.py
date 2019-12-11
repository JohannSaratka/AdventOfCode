'''
Created on 06.12.2019

@author: johann
'''
from enum import IntEnum
from collections import namedtuple

class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    LDA = 3
    STA = 4
    JNZ = 5
    JEZ = 6
    LT = 7
    EQU = 8
    HLT = 99
    
class ParamMode(IntEnum):
    POSITION = 0
    IMMIDIATE = 1  

RegisterEntry = namedtuple('RegisterEntry', ['value', 'mode'])

class CPU(object):
    
    def __init__(self, program):
        self.pc = 0
        self.acc = 0
        self.memory = program.copy()
        self._input = []
        self.output = None
        self.run_mode = True
        self.r = [0] * 3
    
    def get_input(self):
        return self._input.pop(0)

    def set_input(self, value):
        self._input.append(value)
        
    def run(self):
        while(self.run_mode):
            self.ir = self.fetch()
            self.pc += 1
            fun = self.decode()
            self.execute(fun)
            self.store()            
        return self.memory
    
    def fetch(self):
        return self.memory[self.pc]
    
    def decode(self):        
        mode = self.ir // 100
        opcode = self.ir % 100
        
        try:
            fun, num_operands = self.instruction_set[opcode]
            
        except KeyError:
            raise KeyError("Bad instruction creation: " + str(opcode))
        
        self.load_registers(num_operands, mode)
        return fun 
   
    def load_registers(self, num_operands, mode):        
        for reg_idx in range(num_operands): 
            self.r[reg_idx] = RegisterEntry(self.fetch(), (mode % 10))
            
            mode //= 10
            self.pc += 1
            
    def execute(self, fun):
        fun(self)
        
    def store(self):
        if self.dst is not None:
            self.memory[self.dst.value] = self.acc
            
    def get_data(self,reg):
        if reg.mode == ParamMode.POSITION:
            return self.memory[reg.value]
        elif reg.mode == ParamMode.IMMIDIATE:
            return reg.value
    
    def add(self): 
        self.acc = self.get_data(self.r[0]) + self.get_data(self.r[1])
        self.dst = self.r[2]

    def mul(self): 
        self.acc = self.get_data(self.r[0]) * self.get_data(self.r[1])
        self.dst = self.r[2]
        
    def lda(self): 
        self.acc = self.get_input()
        self.dst = self.r[0]

    def sta(self): 
        self.output = self.get_data(self.r[0])
        self.dst = None
        
    def jnz(self):
        if (self.get_data(self.r[0]) != 0):
            self.pc = self.get_data(self.r[1])
            
    def jez(self):
        if (self.get_data(self.r[0]) == 0):
            self.pc = self.get_data(self.r[1])
    
    def lt(self):
        if (self.get_data(self.r[0]) < self.get_data(self.r[1])):
            self.acc = 1
        else:
            self.acc = 0
        self.dst = self.r[2]
            
    def equ(self):
        if (self.get_data(self.r[0]) == self.get_data(self.r[1])):
            self.acc = 1
        else:
            self.acc = 0
        self.dst = self.r[2]
        
    def hlt(self): 
        self.run_mode = False
        self.dst = None
        
    instruction_set = { 
            OpCode.ADD: (add,3),
            OpCode.MUL: (mul,3),
            OpCode.LDA: (lda,1),
            OpCode.STA: (sta,1),
            OpCode.JNZ: (jnz,2),
            OpCode.JEZ: (jez,2),            
            OpCode.LT:  (lt,3),
            OpCode.EQU: (equ,3),
            OpCode.HLT: (hlt,0)
            }
        
def intCodeToList(intCodeProg):
    return [int(x) for x in intCodeProg[0].split(',')]

if __name__ == '__main__':
    pass