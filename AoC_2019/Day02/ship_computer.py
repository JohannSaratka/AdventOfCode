'''
Created on 06.12.2019

@author: johann
'''
from enum import IntEnum

class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    RD = 3
    WRT = 4
    HLT = 99
    
class ParamMode(IntEnum):
    POSITION = 0
    IMMIDIATE = 1  
        
class Instruction(object):
    def __init__(self,mode):
        self.mode = mode        
        self.operands = list()
        
    # Create based on class name:
    def decode(instr):
        instructions = { 
            OpCode.ADD: Add,
            OpCode.MUL: Multiply,
            OpCode.RD:  Read,
            OpCode.WRT: Write,
            OpCode.HLT: Halt
            }
        mode = instr // 100
        opcode = instr % 100
        if opcode not in instructions.keys():
            assert 0, "Bad instruction creation: " + str(opcode)
        else:
            return instructions[opcode](mode)
        
    decode = staticmethod(decode)
            
    def load_operand(self, processor):
        if (self.mode % 10) == ParamMode.POSITION:
            # last operand is destination that is resolved when value is stored
            if len(self.operands) < (self.num_operands - 1):
                self.operands.append(processor.memory[processor.fetch()])
            else:
                self.operands.append(processor.fetch())
        elif (self.mode % 10) == ParamMode.IMMIDIATE:
            self.operands.append(processor.fetch())
        
        self.mode //= 10 
            
    def load_done(self):
        return len(self.operands) == self.num_operands
    
    
class Add(Instruction):
    num_operands = 3

    def execute(self, processor): 
        processor.acc = self.operands[0] + self.operands[1]
        
    def store(self, processor): 
        processor.memory[self.operands[2]] = processor.acc      

class Multiply(Instruction):
    num_operands = 3
        
    def execute(self, processor): 
        processor.acc = self.operands[0] * self.operands[1]
        
    def store(self, processor): 
        processor.memory[self.operands[2]] = processor.acc  

class Read(Instruction):
    num_operands = 1
        
    def execute(self, processor): 
        pass

    def store(self, processor): 
        processor.memory[self.operands[0]] = processor.input

class Write(Instruction):
    num_operands = 1
        
    def execute(self, processor): 
        pass
    
    def store(self, processor): 
        processor.output = processor.memory[self.operands[0]] 
        
class Halt(Instruction):    
    num_operands = 0
        
    def execute(self, processor): 
        processor.run_mode = False
        
    def store(self, processor): 
        pass
        
class ShipComputer():
    def __init__(self, program):
        self.pc = 0
        self.acc = 0
        self.memory = program
        self.input = None
        self.output = None
        self.run_mode = True
        
    def run(self):
        while(self.run_mode):
            instr_register = self.fetch()
            instr = self.decode(instr_register)
            self.pc += 1
            while not instr.load_done():
                instr.load_operand(self)
                self.pc += 1
            instr.execute(self)
            instr.store(self)            
        return self.memory
    
    def fetch(self):
        return self.memory[self.pc]
    
    def decode(self, instr_register):
        return Instruction.decode(instr_register)
    
        
def intCodeToList(intCodeProg):
    return [int(x) for x in intCodeProg[0].split(',')]

if __name__ == '__main__':
    pass