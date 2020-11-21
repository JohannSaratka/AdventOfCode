'''
Created on 25.01.2020

@author: johann

FPS are terrible, drawing the display is not solved properly
'''

import sys
from collections import defaultdict
import threading
import pygame
from pygame.constants import KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_LEFT, K_RIGHT, K_a, K_d
from AoC_2019.common.ship_computer import CPU, intCodeToList


class Event(object):
    def __init__(self, doc=None):
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return EventHandler(self, obj)

    def __set__(self, obj, value):
        pass


class EventHandler(object):
    def __init__(self, event, obj):
        self.event = event
        self.obj = obj

    def _getfunctionlist(self):
        """(internal use) """
        try:
            eventhandler = self.obj.__eventhandler__
        except AttributeError:
            eventhandler = self.obj.__eventhandler__ = {}
        return eventhandler.setdefault(self.event, [])

    def add(self, func):
        """Add new event handler function.

        Event handler function must be defined like func(sender, earg).
        You can add handler also by using '+=' operator.
        """
        self._getfunctionlist().append(func)
        return self

    def remove(self, func):
        """Remove existing event handler function.

        You can remove handler also by using '-=' operator.
        """
        self._getfunctionlist().remove(func)
        return self

    def fire(self, earg=None):
        """Fire event and call all handler functions

        You can call EventHandler object itself like e(earg) instead of
        e.fire(earg).
        """
        for func in self._getfunctionlist():
            func(self.obj, earg)

    __iadd__ = add
    __isub__ = remove
    __call__ = fire


class Game(object):
    bgColor = (255, 255, 255, 255)
    evtKeyUp = Event()
    evtKeyDown = Event()

    def __init__(self, title, size):
        pygame.init()
        self.displaySurface = pygame.display.set_mode(size, 0, 32)
        self.title = title
        pygame.display.set_caption(self.title)
        self.fps = 0
        self.setupGame()

    def setupGame(self):
        raise NotImplementedError

    def setFPS(self, fps):
        self.fps = fps  # frames per second setting
        self.fpsClock = pygame.time.Clock()

    def setBasicFont(self, fontName, fontSize):
        self.basicFont = self.getFont(fontName, fontSize)

    def getFont(self, fontName, fontSize):
        return pygame.font.Font(fontName, fontSize)

    def updateDisplay(self):
        pygame.display.update()
        if self.fps != 0:
            self.fpsClock.tick(self.fps)

    def runGameLoop(self):
        # run the game loop
        while True:
            self.displaySurface.fill(self.bgColor)
            # -----------
            self.handleEvents()
            self.updateGameState()
            # -----------
            self.updateDisplay()

    def updateGameState(self):
        raise NotImplementedError

    def handleEvents(self):
        self.checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                self.evtKeyUp(event)
            elif event.type == KEYDOWN:
                self.evtKeyDown(event)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate()
                # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event)  # put the other KEYUP event objects back

    def checkForKeyPress(self):
        """
        Go through event queue looking for a KEYUP event.
        Grab KEYDOWN events to remove them from the event queue.
        """
        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None


WINDOWWIDTH = 640
WINDOWHEIGHT = 600


class Arcade(Game):
    basicFontName = 'couriernew'
    basicFontSize = 18

    def __init__(self,  title, size, program):
        self.cart = Cartridge(program, self.sync)
        super(Arcade, self).__init__(title, size)

    def setupGame(self):
        self.bgColor = (0, 0, 0, 0)
        self.setFPS(30)
        self.setBasicFont(pygame.font.match_font(
            self.basicFontName), self.basicFontSize)

        self.evtKeyDown += self.handleKeyDownEvent

        self.initGameState()

    def initGameState(self):
        self.cart_thread = threading.Thread(target=self.cart.brain.run)
        self.sync_event = threading.Event()
        self.draw_event = threading.Event()
        self.screen_draw_pos = 10, 10
        self.cart_thread.start()
        self.fps_count = 0

    def sync(self):
        self.sync_event.set()
        self.draw_event.wait()
        self.sync_event.clear()
        return self.cart.set_input()

    def handleKeyDownEvent(self, sender, event):
        if event.key in (K_LEFT, K_a):
            pass
        elif event.key in (K_RIGHT, K_d):
            pass

    def updateGameState(self):
        if self.fps_count == 0:
            self.draw_event.clear()
        if not self.cart.brain.run_mode:
            self.showGameOverScreen()

        caption = self.cart.draw_screen()
        for line_num, line in enumerate(caption.split('\n')):
            surf = self.basicFont.render(line, True, (255, 255, 255, 255))
            rect = (self.screen_draw_pos[0], self.screen_draw_pos[1] +
                    (line_num * self.basicFontSize) + (3 * line_num))
            self.displaySurface.blit(surf, rect)

        surf_score = self.basicFont.render(
            str(self.cart.score), True, (255, 255, 255, 255))
        self.displaySurface.blit(surf_score, (0, 0))

        if self.fps_count == 10:
            self.fps_count = 0
            self.sync_event.wait()
            self.draw_event.set()
        else:
            self.fps_count += 1

    def showGameOverScreen(self):
        surf_score = self.basicFont.render(
            str(self.cart.score), True, (255, 255, 255, 255))
        self.displaySurface.blit(surf_score, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress()  # clear out any key presses in the event queue

        while True:
            if self.checkForKeyPress():
                pygame.event.get()  # clear event queue
                self.initGameState()
                return


class Cartridge(object):
    def __init__(self, program, get_input):
        program[0] = 2
        self.brain = CPU(program)
        self.brain.get_input = get_input
        self.brain.set_output = self.set_output
        self.grid = defaultdict(int)
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.score = 0
        self.output = []

    def set_output(self, out):
        self.output.append(out)
        if len(self.output) == 3:
            if self.output[0] == -1 and self.output[1] == 0:
                self.score = self.output[2]
            else:
                self.grid[(self.output[0], self.output[1])] = self.output[2]
                if self.output[2] == 3:
                    self.paddle = (self.output[0], self.output[1])
                elif self.output[2] == 4:
                    self.ball = (self.output[0], self.output[1])
            self.output.clear()

    def set_input(self):
        if self.paddle[0] < self.ball[0]:
            return 1
        elif self.paddle[0] > self.ball[0]:
            return -1
        else:
            return 0

    def draw_screen(self):
        grid_coords = self.grid.keys()
        max_x = max(grid_coords, key=lambda coord: coord[0])[0]
        max_y = max(grid_coords, key=lambda coord: coord[1])[1]
        hull_drawing = [''] * (max_y + 1)
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if self.grid[(x, y)] == 1:
                    hull_drawing[y] += '#'
                elif self.grid[(x, y)] == 2:
                    hull_drawing[y] += 'X'
                elif self.grid[(x, y)] == 3:
                    hull_drawing[y] += '='
                elif self.grid[(x, y)] == 4:
                    hull_drawing[y] += 'O'
                else:
                    hull_drawing[y] += ' '
        return "\n".join(hull_drawing)

