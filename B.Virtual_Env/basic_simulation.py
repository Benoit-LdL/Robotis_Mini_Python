#!/usr/bin/env python3

from klampt import *
from klampt.model import coordinates
import time, math

from numpy import angle, full

##############__SETTINGS__##############
worldFile = "test_world.xml"
sleepTime = 0.1
show_labels = False
########################################

if __name__ == "__manin__":
    
    world = WorldModel()
    res = world.readFile(worldFile)
    if res: RuntimeError("Unable to load world file")
    sim = Simulator(world)
    
    mini        = world.robot(0)

    numLinks    = mini.numLinks() 
    numDrivers  = mini.numDrivers()

    coordinates.setWorldModel(world)

    vis.add("world",world)
    if (show_labels):
        vis.add("coordinates", coordinates.manager())
    vis.show()

    iteration   = 0
    joint_angle = 0.0
    joint       = 0
    while vis.shown():
        vis.lock()
        
        #this updates the coordinates module
        coordinates.updateFromWorld()
        
        vis.unlock()
        sim.simulate(sleepTime)
        