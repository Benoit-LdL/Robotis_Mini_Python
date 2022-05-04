#!/usr/bin/env python3

import klampt
from klampt import vis
from klampt.vis import GLRealtimeProgram

class GLTest(GLRealtimeProgram):
    """Define hooks into the GUI loop to draw and update the simulation"""
    def __init__(self,world,sim):
        GLRealtimeProgram.__init__(self,"GLTest")
        self.world = world
        self.sim = sim
        self.traj = klampt.model.trajectory.RobotTrajectory(self.world.robot(0))
        self.traj.load("/home/benoit/Desktop/motion-planner/klampt_env/library_examples/data/motions/athlete_flex_opt.path")

    def display(self):
        self.sim.updateWorld()
        self.world.drawGL()

    def idle(self):
        sim = self.sim
        traj = self.traj
        starttime = 2.0
        if sim.getTime() > starttime:
            (q,dq) = (traj.eval(self.sim.getTime()-starttime),traj.deriv(self.sim.getTime()-starttime))
            sim.controller(0).setPIDCommand(q,dq)
        sim.simulate(self.dt)
        return

if __name__ == "__main__":
    print("================================================================")
    print("gl_vis.py: This example demonstrates how to use the GL visualization interface")
    print("   to tie directly into the GUI.")
    print()
    print("   The demo simulates a world and reads a force sensor")
    print("================================================================")
    world = klampt.WorldModel()
    res = world.readFile("test_world.xml")
    if not res:
        raise RuntimeError("Unable to load world")
    sim = klampt.Simulator(world)
    print("STARTING vis.run()")
    vis.run(GLTest(world,sim))
    print("END OF vis.run()")
