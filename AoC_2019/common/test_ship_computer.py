'''
Created on 06.12.2019

@author: johann
'''
import unittest
import ship_computer

class Test(unittest.TestCase):
    def assertProgramExecution(self, initial_memory, expected_memory):
        ship = ship_computer.CPU(initial_memory)
        self.assertEqual(ship.run(), expected_memory)
    
    def assertGivenInputExpectedOutput(self, initial_memory, given_input, expected_output):
        ship = ship_computer.CPU(initial_memory)
        ship.set_input(given_input)
        ship.run()
        self.assertEqual(ship.get_output(), expected_output)
        
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
        
    def testInputToOutput(self):
        self.assertGivenInputExpectedOutput([3,0,4,0,99],'A','A')
        
    def testParameterModes(self):
        self.assertProgramExecution([1002,4,3,4,33], [1002,4,3,4,99])
    
    def testInputEqualToEightPositionMode(self):
        self.assertGivenInputExpectedOutput([3,9,8,9,10,9,4,9,99,-1,8],8,1)
        self.assertGivenInputExpectedOutput([3,9,8,9,10,9,4,9,99,-1,8],4,0)
        
    def testInputLessThanEightPositionMode(self):
        self.assertGivenInputExpectedOutput([3,9,7,9,10,9,4,9,99,-1,8],8,0)
        self.assertGivenInputExpectedOutput([3,9,7,9,10,9,4,9,99,-1,8],4,1)
        
    def testInputEqualToEightImmidiateMode(self):
        self.assertGivenInputExpectedOutput([3,3,1108,-1,8,3,4,3,99],8,1)
        self.assertGivenInputExpectedOutput([3,3,1108,-1,8,3,4,3,99],4,0)
        
    def testInputLessThanEightImmidiateMode(self):
        self.assertGivenInputExpectedOutput([3,3,1107,-1,8,3,4,3,99],8,0)
        self.assertGivenInputExpectedOutput([3,3,1107,-1,8,3,4,3,99],4,1)
    
    def testInputEqualZeroWithJumpPositionMode(self):
        self.assertGivenInputExpectedOutput([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],0,0)
        self.assertGivenInputExpectedOutput([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],4,1)

    def testInputEqualZeroWithJumpImmediateMode(self):
        self.assertGivenInputExpectedOutput([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],0,0)
        self.assertGivenInputExpectedOutput([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],4,1)
        
    def testMoreComplexExample(self):
        program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        
        self.assertGivenInputExpectedOutput(program, 4, 999)
        self.assertGivenInputExpectedOutput(program, 8, 1000)
        self.assertGivenInputExpectedOutput(program, 12, 1001)
        
    def testOutputQuine(self):
        ship = ship_computer.CPU([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
        ship.run()
        self.assertEqual(ship.get_output(), [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
        
    def testOutput16Digits(self):
        ship = ship_computer.CPU([1102,34915192,34915192,7,4,7,99,0])
        ship.run()
        self.assertEqual(ship.get_output(), 34915192*34915192)
        
    def testLargeNumber(self):
        ship = ship_computer.CPU([104,1125899906842624,99])
        ship.run()
        self.assertEqual(ship.get_output(), 1125899906842624)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()