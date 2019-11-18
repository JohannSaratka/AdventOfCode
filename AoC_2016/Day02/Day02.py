'''
--- Day 2: Bathroom Security ---
You arrive at Easter Bunny Headquarters under cover of darkness. However, 
you left in such a rush that you forgot to use the bathroom! Fancy office 
buildings like this one usually have keypad locks on their bathrooms, so 
you search the front desk for the code.
"In order to improve security," the document you find says, "bathroom codes 
will no longer be written down. Instead, please memorize and follow the 
procedure below to access the bathrooms."
The document goes on to explain that each button to be pressed can be found 
by starting on the previous button and moving to adjacent buttons on the 
keypad: U moves up, D moves down, L moves left, and R moves right. Each 
line of instructions corresponds to one button, starting at the previous 
button (or, for the first line, the "5" button); press whatever button 
you're on at the end of each line. If a move doesn't lead to a button, 
ignore it.
You can't hold it much longer, so you decide to figure out the code as you 
walk to the bathroom. You picture a keypad like this:
1 2 3
4 5 6
7 8 9
'''
import unittest

class TestGetShortestPathDestination(unittest.TestCase):
    def test_getNextButton_stepOne(self):
        self.assertEqual(getNextButton(5,'ULL'), 1, "")
    def test_getNextButton_stepTwo(self):
        self.assertEqual(getNextButton(1,'RRDDD'), 9, "")
    def test_getNextButton_stepThree(self):
        self.assertEqual(getNextButton(9,'LURDL'), 8, "")
    def test_getNextButton_stepFour(self):
        self.assertEqual(getNextButton(8,'UUUUD'), 5, "")
    def test_getNextButtonPartTwo_stepOne(self):
        self.assertEqual(getNextButtonPartTwo(5,'ULL'), 5, "")
    def test_getNextButtonPartTwo_stepTwo(self):
        self.assertEqual(getNextButtonPartTwo(5,'RRDDD'), 0xD, "")
    def test_getNextButtonPartTwo_stepThree(self):
        self.assertEqual(getNextButtonPartTwo(0xD,'LURDL'), 0xB, "")
    def test_getNextButtonPartTwo_stepFour(self):
        self.assertEqual(getNextButtonPartTwo(0xB,'UUUUD'), 3, "")  
          
def getNextButton(startNum,instructions):
    buttonDict={1:['D','R'],
                2:['L','R','D'],
                3:['D','L'],
                4:['U','R','D'],
                5:['U','D','L','R'],
                6:['U','D','L'],
                7:['U','R'],
                8:['U','L','R'],
                9:['U','L']
                }
    moveDict={'D':3,'U':-3,'L':-1,'R':+1}
    for move in instructions:
        startNum += moveDict[move] if move in buttonDict[startNum] else 0   
    return startNum

'''
--- Part Two ---
You finally arrive at the bathroom (it's a several minute walk from 
the lobby so visitors can behold the many fancy conference rooms and 
water coolers on this floor) and go to punch in the code. Much to your 
bladder's dismay, the keypad is not at all like you imagined it. Instead, 
you are confronted with the result of hundreds of man-hours of 
bathroom-keypad-design meetings:
    1
  2 3 4
5 6 7 8 9
  A B C
    D
'''
def getNextButtonPartTwo(startNum,instructions):
    buttonDict={0x1:{'D':3},
                0x2:{'R':3,'D':6},
                0x3:{'U':1,'D':7,'L':2,'R':4},
                0x4:{'L':3,'D':8},
                0x5:{'R':6},
                0x6:{'U':2,'D':0xA,'L':5,'R':7},
                0x7:{'U':3,'D':0xB,'L':6,'R':8},
                0x8:{'U':4,'D':0xC,'L':7,'R':9},
                0x9:{'L':8},
                0xA:{'U':6,'R':0xB},
                0xB:{'U':7,'D':0xD,'L':0xA,'R':0xC},
                0xC:{'U':8,'L':0xB},
                0xD:{'U':0xB},
                }
    for move in instructions:
        startNum = buttonDict[startNum][move] if move in buttonDict[startNum] else startNum   
    return startNum

if __name__ == '__main__':
    with open('Day02Data.txt','r')as inputFile:
        button=5
        for line in inputFile:            
            #button=getNextButton(button,line)            
            #print button
            button=getNextButtonPartTwo(button,line)            
            print hex(button)