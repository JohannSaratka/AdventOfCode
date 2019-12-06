'''
Created on 06.12.2019

@author: johann
'''
import unittest
import ship_computer

class Test(unittest.TestCase):
    def assertProgramExecution(self,initial_memory, expected_memory):
        ship = ship_computer.ShipComputer(initial_memory)
        self.assertEqual(ship.run(), expected_memory)
        
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
        
    def testInputOutput(self):
        ship = ship_computer.ShipComputer([3,0,4,0,99])
        ship.input = 'a'
        self.assertEqual(ship.output, None)
        self.assertEqual(ship.run(), ['a',0,4,0,99])
        self.assertEqual(ship.output, 'a')
        
    def testParameterModes(self):
        self.assertProgramExecution([1002,4,3,4,33], [1002,4,3,4,99])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()