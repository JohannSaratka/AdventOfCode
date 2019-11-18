'''
Created on 01.12.2017

--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?
--- Part Two ---

To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?

'''

import re
from collections import Counter


class Vector3d(object):
    def __init__(self, x=0, y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return "(%s, %s, %s)"%(self.x, self.y, self.z)
    
    def __add__(self,other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented
    
class Particle(object):
    def __init__(self,init_str,id):
        init_values = re.findall(r'(-?\d+,-?\d+,-?\d+)',init_str)
        self.pos=Vector3d(*map(int,init_values[0].split(',')))
        self.vel=Vector3d(*map(int,init_values[1].split(',')))
        self.acc=Vector3d(*map(int,init_values[2].split(',')))
        self.id = id
        
    def __repr__(self):
        return "(%s, %s, %s)"%( self.pos.x, self.pos.y, self.pos.z)
    
    def sim(self):
        self.vel+=self.acc
        self.pos+=self.vel
        
    def distance(self):
        return abs(self.pos.x)+abs(self.pos.y)+abs(self.pos.z)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pos == other.pos
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented
    
    def __hash__(self):
        return hash(self.__repr__())
    
def solve(input_list):
    particle_list=list()
    min_dist=50000000000
    id_of_min_dist=0
    count = 0
    for n,item in enumerate(input_list):
        particle_list.append(Particle(item,n))
    while count<2000:
        map(lambda x: x.sim(), particle_list)
        particle_list.sort(key=lambda x: x.distance())
        print particle_list[0].id, particle_list[0].distance()
        if particle_list[0].distance() < min_dist:
            min_dist=particle_list[0].distance()
            id_of_min_dist = particle_list[0].id             
        else:
            count+=1
    return id_of_min_dist 

def solvePartTwo(input_list):
    particle_list=list()
    num_particles=2000
    count = 0
    for n,item in enumerate(input_list):
        particle_list.append(Particle(item,n))
    while count < 2000:
        if len(set(particle_list))< len(particle_list):
            counted_particles=Counter(particle_list)
            particle_list=[k for k,v in counted_particles.iteritems() if v==1]
        map(lambda x: x.sim(), particle_list)
        if num_particles > len(particle_list):
            num_particles= len(particle_list)            
        else:
            count+=1
    return num_particles 


if __name__ == "__main__":
    with open("input.txt",'r') as inFile:           
        puzzleInput = inFile.read().rstrip()
        #print solve(puzzleInput.split('\n'))
        print solvePartTwo(puzzleInput.split('\n'))