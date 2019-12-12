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
    ARB = 9
    HLT = 99
    
class ParamMode(IntEnum):
    POSITION = 0
    IMMIDIATE = 1
    RELATIVE = 2

RegisterEntry = namedtuple('RegisterEntry', ['value', 'mode'])

class CPU(object):
    
    def __init__(self, program):
        self.pc = 0
        self.acc = 0
        self.memory = {key:value for key,value in enumerate(program)}
        self._input = []
        self._output = []
        self.run_mode = True
        self.r = [0] * 3
        self.base = 0
                    
    def get_input(self):
        return self._input.pop(0)

    def set_input(self, value):
        self._input.append(value)
        
    def get_output(self):
        if len(self._output) == 1:
            return self._output.pop(0)
        else:
            return self._output

    def set_output(self, value):
        self._output.append(value)
        
    def run(self):
        while(self.run_mode):
            self.ir = self.fetch()
            self.pc += 1
            fun = self.decode()
            self.execute(fun)
            self.store()            
        return [self.memory[key] for key in sorted(self.memory.keys())]
    
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
            self.set_data(self.dst)
            
    def get_data(self, reg):
        if reg.mode == ParamMode.POSITION:
            return self.memory.get(reg.value, 0)
        elif reg.mode == ParamMode.IMMIDIATE:
            return reg.value
        elif reg.mode == ParamMode.RELATIVE:
            return self.memory.get(reg.value + self.base, 0)
        
    def set_data(self, reg):
        if reg.mode == ParamMode.POSITION:
            self.memory[reg.value] = self.acc
        elif reg.mode == ParamMode.RELATIVE:
            self.memory[reg.value + self.base] = self.acc
            
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
        self.set_output(self.get_data(self.r[0]))
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
        
    def arb(self): 
        self.base += self.get_data(self.r[0])
        self.dst = None
        
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
            OpCode.ARB: (arb,1),
            OpCode.HLT: (hlt,0)
            }
        
def intCodeToList(intCodeProg):
    return [int(x) for x in intCodeProg[0].split(',')]

if __name__ == '__main__':
    pass