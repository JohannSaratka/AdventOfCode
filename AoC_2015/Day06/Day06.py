'''
Created on 03.12.2015

@author: Johann
'''
import unittest
import re
from PIL import Image, ImageDraw


class Test(unittest.TestCase):
    def test_readInstructions_turnOnEveryLight(self):
        self.assertEqual(readInstruction("turn on 0,0 through 999,999"), (ON,(0,0),(999,999)))
    def test_readInstructions_toggleRow(self):
        self.assertEqual(readInstruction("toggle 0,0 through 999,0"), (TOGGLE,(0,0),(999,0)))
    def test_readInstructions_turnOffFourLights(self):
        self.assertEqual(readInstruction("turn off 499,499 through 500,500"), (OFF,(499,499),(500,500)))
        
    def test_flipSwitch_ToggleOn(self):
        self.assertEqual(flipSwitch(TOGGLE, (0,0), (999,0)), 1000)
    def test_flipSwitch_ToggleOff(self):
        self.assertEqual(flipSwitch(ON, (0,0), (999,999)), 1000000)
        self.assertEqual(flipSwitch(TOGGLE, (0,0), (999,0)), 999000)
    def test_flipSwitch_turnOnEveryLight(self):
        self.assertEqual(flipSwitch(ON, (0,0), (999,999)), 1000000)
    def test_flipSwitch_turnOffEveryLight(self):
        self.assertEqual(flipSwitch(ON, (0,0), (999,999)), 1000000)
        self.assertEqual(flipSwitch(OFF, (0,0), (999,999)), 0)
    def test_flipSwitch_turnOffFourLights(self):
        self.assertEqual(flipSwitch(ON, (0,0), (999,999)), 1000000)
        self.assertEqual(flipSwitch(OFF, (499,499), (500,500)), 999996)
    
    def test_dimLights_turnOnOne(self):
        self.assertEqual(dimLights(ON, (0,0), (0,0)), 1)
    def test_dimLights_toggleAll(self):
        self.assertEqual(dimLights(TOGGLE, (0,0), (999,999)), 2000000)
    
    def setUp(self):
        global grid
        grid=Image.new("L", (1000,1000))
ON=1
OFF=-1
TOGGLE=2

grid=Image.new("L", (1000,1000))

def readInstruction(instr):
    switch,startX,startY,endX,endY=re.findall(r"(\S+)\s(\d*),(\d*)\D*(\d*),(\d*)", instr)[0]
    if switch=='toggle':switch=TOGGLE
    if switch=='on':switch=ON
    if switch=='off':switch=OFF
    return (switch,(int(startX),int(startY)),(int(endX),int(endY)))

def flipSwitch(switch,start,end):
    global grid
    draw=ImageDraw.Draw(grid)
    if switch==ON:
        draw.rectangle([start,end], fill=1)
    if switch==OFF:
        draw.rectangle([start,end], fill=0)
    if switch==TOGGLE:
        pix=grid.load()
        for x in xrange(start[0],end[0]+1):
            for y in xrange(start[1],end[1]+1):
                value= not pix[x,y]
                pix[x,y]=value
    lightCount=grid.getcolors()
    if len(lightCount)==1:
        return lightCount[0][0]*lightCount[0][1]
    else:
        return lightCount[1][0]

def dimLights(switch,start,end):
    global grid    
    pix=grid.load()
    for x in xrange(start[0],end[0]+1):
        for y in xrange(start[1],end[1]+1):
            newvalue=pix[x,y]+switch
            pix[x,y]=newvalue if newvalue>0 else 0
    lightCount=grid.getcolors()
    brightness =sum([x[0]*x[1] for x in lightCount])
    return brightness
    

if __name__ == "__main__":
    #unittest.main()
    with open('Day06Data.txt','r')as name:
        for line in name:
            switch, start, end=readInstruction(line)
            #print flipSwitch(switch, start, end)
            print dimLights(switch, start, end)
    