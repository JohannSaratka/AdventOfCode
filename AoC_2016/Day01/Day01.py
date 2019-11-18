'''
--- Day 1: No Time for a Taxicab ---
Santa's sleigh uses a very high-precision clock to guide its movements, 
and the clock's oscillator is regulated by stars. Unfortunately, the stars 
have been stolen... by the Easter Bunny. To save Christmas, Santa needs you 
to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on 
each day in the advent calendar; the second puzzle is unlocked when you 
complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. 
"Near", unfortunately, is as close as you can get - the instructions 
on the Easter Bunny Recruiting Document the Elves intercepted start 
here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates 
(where you just landed) and face North. Then, follow the provided 
sequence: either turn left (L) or right (R) 90 degrees, then walk forward 
the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, 
so you take a moment and work out the destination. Given that you can 
only walk on the street grid of the city, how far is the shortest path 
to the destination?
'''
import unittest

class TestGetShortestPathDestination(unittest.TestCase):
    def test_getPath_isFive(self):
        self.assertEqual(getPath('R2, L3'), 5, "")
    def test_getPath_isTwo(self):
        self.assertEqual(getPath('R2, R2, R2'), 2, "")
    def test_getPath_isTwelve(self):    
        self.assertEqual(getPath('R5, L5, R5, R3'), 12, "")
    def test_getPath_longerSteps(self):    
        self.assertEqual(getPath('R50, L5'), 55, "")
    def test_visitedTwice(self):
        self.assertEqual(getVisited('R8, R4, R4, R8'), 4, "")

def getPath(path):
    pathList=path.replace(',','').split()
    pos=[0,0]
    num=0    
    visited=[pos[:]]
    face='N'
    grid={'N':{'R':(1,'O'),'L':(-1,'W')},
          'S':{'R':(-1,'W'),'L':(1,'O')},
          'O':{'R':(-1,'S'),'L':(1,'N')},
          'W':{'R':(1,'N'),'L':(-1,'S')},}
    for step in pathList:        
        direction,face=grid[face][step[0]]
        last=pos[:]
        pos[num%2]+=int(step[1:])*direction
        visited.append(pos[:])
        num+=1
        #print step,pos    
    return abs(pos[0])+abs(pos[1])   
'''
--- Part Two ---
Then, you notice the instructions continue on the back of the Recruiting 
Document. Easter Bunny HQ is actually at the first location you visit 
twice.
For example, if your instructions are R8, R4, R4, R8, the first location 
you visit twice is 4 blocks away, due East.
How many blocks away is the first location you visit twice?
''' 
def getVisited(path):
    pathList=path.replace(',','').split()
    pos=[0,0]
    num=0
    visited=[pos[:]]
    face='N'
    grid={'N':{'R':(1,'O'),'L':(-1,'W')},
          'S':{'R':(-1,'W'),'L':(1,'O')},
          'O':{'R':(-1,'S'),'L':(1,'N')},
          'W':{'R':(1,'N'),'L':(-1,'S')},}
    done=False
    for step in pathList:        
        direction,face=grid[face][step[0]]
        for i in xrange(int(step[1:])):
            pos[num%2]+=direction
        
            if pos in visited:
                done=True
                break
            visited.append(pos[:])
            #print step,pos
        num+=1
        if done:
            break
    #print step,pos   
    return abs(pos[0])+abs(pos[1])   
                
debug=0
if __name__ == '__main__':
    if debug==1:    
        unittest.main()
    else:
        with open('Day01Data.txt','r')as name:
            for s in name:            
                print getPath(s)
                print getVisited(s)