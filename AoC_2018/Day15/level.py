'''
Created on 15.12.2018

@author: johann
'''
import numpy as np

class GameState(object):
    def __init__(self):
        self.elfs = {}
        self.goblins = {}
        
class Level(object):
    def __init__(self,mapTextLines):
        '''Convert the text in mapTextLines into a level object.'''

        # Create empty starting game state object.
        self.gameState = GameState()
        
        self.width = len(mapTextLines[0])
        self.height = len(mapTextLines)

        self.spriteGrid = np.full((self.width, self.height), True)
        
        for y,mapLine in enumerate(mapTextLines):
            for x, mapChar in enumerate(mapLine):
                # Loop through the spaces in the map and find the G and E
                # characters for the starting game state.
                if mapChar=='G':
                    self.gameState.goblins[(x,y)] = Unit()
                    mapChar='.'
                elif mapChar=='E':
                    self.gameState.elfs[(x,y)] = Unit()
                    mapChar='.'
                
                if mapChar=='.':
                    self.spriteGrid[x][y] = False

    
    def draw(self,mapSurf):
        text = text.replace('1f401268', '')
        label = myFont.render(text, at, ERRORCOLOR, bg)
        SCREEN.blit(label, (x, y))
        
            
    def movePlayer(self,moveVector):
        """Given a map and game state object, see if it is possible for the
        player to make the given move. If it is, then change the player's
        position (and the position of any pushed star). If not, do nothing.
    
        Returns True if the player moved, otherwise False."""
    
        # The code for handling each of the directions is so similar aside
        # from adding or subtracting 1 to the x/y coordinates. We can
        # simplify it by using the xOffset and yOffset variables.
        
        newPlayerPos = self.gameState.player.pos + moveVector 
    
        # See if the player can move in that direction.
        if self.isWall(newPlayerPos.x, newPlayerPos.y):
            return False
        else:
            for key,star in self.gameState.stars.items():
                if newPlayerPos == star.pos:
                    newStarPos = star.pos + moveVector
                    # There is a star in the way, see if the player can push it.
                    if not self.isBlocked(newStarPos.x,newStarPos.y):
                        star.pos = newStarPos
                        self.gameState.stars[newStarPos.toTuple()] = star
                        del self.gameState.stars[key]
                        break
                    else:
                        return False
            # Move the player upwards.
            self.gameState.player.pos = newPlayerPos
            return True

    def isWall(self, x, y):
        """Returns True if the (x, y) position on
        the map is a wall, otherwise return False."""
        return self.spriteGrid[x][y]

    def isBlocked(self, x, y):
        """Returns True if the (x, y) position on the map is
        blocked by a wall or star, otherwise return False."""
        return (self.isWall(x, y) 
                or (x, y) in self.gameState.elfs 
                or (x, y) in self.gameState.goblins)
        