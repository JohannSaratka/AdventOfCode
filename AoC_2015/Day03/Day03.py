'''
Created on 03.12.2015

@author: Johann
'''
import unittest


class Test(unittest.TestCase):
    def test_DeliverPresents_OneDir(self):
        self.assertEqual(deliverPresents('>'), 2, "")
        
    def test_DeliverPresents_Square(self):
        self.assertEqual(deliverPresents('^>v<'), 4, "")
    
    def test_DeliverPresents_LuckyChildren(self):
        self.assertEqual(deliverPresents('^v^v^v^v^v'), 2, "")
        
    def test_roboDeliverPresents_OneDir(self):
        self.assertEqual(roboDeliverPresents('^v'), 3, "")
        
    def test_roboDeliverPresents_Square(self):
        self.assertEqual(roboDeliverPresents('^>v<'), 3, "")
    
    def test_roboDeliverPresents_LuckyChildren(self):
        self.assertEqual(roboDeliverPresents('^v^v^v^v^v'), 11, "")
        
    def tearDown(self):
        Deliverer.visitedHouses=set()
        
class Pos(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def __iadd__(self,other):        
        return Pos(self.x + other.x,self.y + other.y)
    
    def __repr__(self):
        return "(%d,%d)" % (self.x,self.y)
    
    def __eq__(self,other):
        if isinstance(other,Pos):
            return ((self.x==other.x) and (self.y==other.y))
        else: 
            return False
        
    def __ne__(self, other):
        return (not self.__eq__(other))
    
    def __hash__(self):
        return hash(self.__repr__())
    
class Deliverer(object):
    visitedHouses=set()
    posDict={'<':Pos(0,-1), # west
           '>':Pos(0,1 ),# east
           '^':Pos(-1,0), # north
           'v':Pos( 1,0), # south
           }

    def __init__(self):
        self.pos=Pos(0,0)   
        Deliverer.visitedHouses.add(self.pos)
    def move(self,step):
        self.pos += self.posDict[step]
        Deliverer.visitedHouses.add(self.pos)

directionDict={'<':[0,-1], # west
               '>':[0, 1], # east
               '^':[-1,0], # north
               'v':[ 1,0], # south
               }
def deliverPresents(directions):
    curPosition=[0,0]
    visitedHouses=[curPosition]
    for step in directions:        
        curPosition=map(sum,zip(curPosition,directionDict[step]))
        if curPosition not in visitedHouses:
            visitedHouses.append(curPosition)
    return len(visitedHouses)

def roboDeliverPresents(directions):
    santa=Deliverer()
    robo=Deliverer()
    for num,step in enumerate(directions):        
        if num%2==0:    santa.move(step)  
        else:           robo.move(step)
            
    return len(Deliverer.visitedHouses)

if __name__ == "__main__":
    #unittest.main()
    with open('Day03Data.txt','r')as name:
        for line in name:
            print deliverPresents(line)
            print deliverPresents(line[0::2]) + deliverPresents(line[1::2])
            print roboDeliverPresents(line)