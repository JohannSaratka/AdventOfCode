'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

from tools.Game import Game

def solve(plants_instructions, generations=20):    
    pass

def solvePartTwo(license_file):
    pass

class Starpusher(Game):
    def setupGame(self):
        self.bgColor = BRIGHTBLUE
        self.setFPS(30)
        #pygame.font.SysFont("consolas", 15)
        self.setBasicFont('freesansbold.ttf', 15)
        self.allLevelList = self.readLevelsFile('testmap1.txt')
        self.setupLevel( self.currentLevelIndex)
        
    def setupLevel(self, levelNum):
        self.currentLevel = copy.deepcopy(self.allLevelList[levelNum])
        self.currentLevel.decorateMap()
        
        self.mapNeedsRedraw = True # set to True to call drawMap()
        
    def readLevelsFile(self,filename):
        with open(filename, 'r') as mapFile:       
            level = Level(mapFile.readlines())
        return level
    
    def updateGameState(self):
        if not self.levelIsComplete:
            # increment the step counter.
            self.mapNeedsRedraw = True


        self.displaySurface.fill(BGCOLOR)

        if self.mapNeedsRedraw:
            self.mapSurf = self.drawMap(self.currentLevel.spriteGrid)
            self.mapNeedsRedraw = False

        # Adjust mapSurf's Rect object based on the camera offset.
        mapSurfRect = self.mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH + self.cam.offsetX, 
                              HALF_WINHEIGHT + self.cam.offsetY)

        # Draw mapSurf to the self.displaySurface Surface object.
        self.displaySurface.blit(self.mapSurf, mapSurfRect)


if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        newGame = Starpusher('StarPusher',(WINWIDTH, WINHEIGHT))
        newGame.runGameLoop()

    