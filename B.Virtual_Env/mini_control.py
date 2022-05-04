#!/usr/bin/env python3

from klampt import *
from klampt.model import coordinates, ik
import time, math

from numpy import angle, full

#   see gpu usage in cli:
#   watch -n 1 nvidia-smi

##############__SETTINGS__##############
worldFile = "test_world.xml"
sleepTime = 0.01
show_labels = False
max_angle = 45
movement = True
########################################

mini_links = [  15, # l_hip         0       ##############__Mini Link Numbers__##############
                19, # l_thigh       1       38  l_shoulder_link                     86  r_shoulder_link
                23, # l_knee        2       41  l_biceps_link                       89  r_biceps_link
                27, # l_ankle       3       45  l_elbow_link                        93  r_elbow_link
                31, # l_foot        4

                38, # l_shoulder    5               15  l_hip_link          63  r_hip_link
                41, # l_biceps      6               19  l_thigh_link        67  r_thigh_link
                45, # l_elbow       7               23  l_knee_link         71  r_knee_link
                    #                               27  l_ankle_link        75  r_ankle_link
                63, # r_hip         8               31  l_foot_link         79  r_foot_link
                67, # r_thigh       9
                71, # r_knee        10
                75, # r_ankle       11
                79, # r_foot        12

                86, # r_shoulder    13
                89, # r_biceps      14
                93] # r_elbow       15

mini_links_l_arm = [38, 41, 45]         # Last element is end effector
mini_links_r_arm = [86, 89, 93]         # Last element is end effector
mini_links_l_leg = [15, 19, 23, 27, 31] # Last element is end effector
mini_links_r_leg = [63, 67, 71, 75, 79] # Last element is end effector

#################################################

def CM2M(cm):                                   # Convert centimeters to meters (klampt coords are in meter)
    return cm/100.0

def MM2M(mm):                                   # Convert milimeters to meters (klampt coords are in meter)
    return mm/1000.0                              

def GetTrimmedConfig(full_config):              # Convert the full config to a trimmed version with only moving links
    full_config = mini.getConfig()
    trimmed_config = []
    for x in range(0,16):
        trimmed_config.append(full_config[mini_links[x]])
    return trimmed_config

def GetFullConfig(trimmed_config):              # Converted config containing moving links to the complete config
    full_config = [0] * 110
    for x in range(0,len(trimmed_config)):
        full_config[mini_links[x]] = trimmed_config[x]
    return full_config

def Local2WorldPos(robotlink,localpos=[0,0,0]):
    obj = ik.objective(robotlink,local=localpos,world=[0,0,0])
    (local,world) = obj.getPosition()
    localToWorld = robotlink.getWorldPosition(local)
    
    # print("## Debug GetLocalPos func ##")
    # print("local to world: " +  str(localToWorld))
    # print("############################")

    return localToWorld

if __name__ == "__main__" :
    world = WorldModel()
    res = world.readFile(worldFile)
    if not res: RuntimeError("Unable to load world file")

    mini        = world.robot(0)

    numLinks    = mini.numLinks() 
    numDrivers  = mini.numDrivers()

    arm_l_linkIndex = mini_links_l_arm[len(mini_links_l_arm)-1]
    arm_r_linkIndex = mini_links_r_arm[len(mini_links_r_arm)-1]
    leg_l_linkIndex = mini_links_l_leg[len(mini_links_l_leg)-1]
    leg_r_linkIndex = mini_links_r_leg[len(mini_links_r_leg)-1]

    arm_l_link = mini.link(arm_l_linkIndex)
    arm_r_link = mini.link(arm_r_linkIndex)
    leg_l_link = mini.link(leg_l_linkIndex)
    leg_r_link = mini.link(leg_r_linkIndex)

    coordinates.setWorldModel(world)

    arm_l_localpos = [0,0,0]    # end effector local position origin offset
    arm_r_localpos = [0,0,0]    #
    leg_l_localpos = [0,0,0]    #
    leg_r_localpos = [0,0,0]    #

    vis.add("world",world)
    
    if (show_labels):
        vis.add("coordinates", coordinates.manager())
    vis.show()
    iteration   = 0
    joint_angle = 0.0
    joint       = 0
    while vis.shown():
        vis.lock()
        
        new_config = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        new_config[joint] = joint_angle*(math.pi/180)
        mini.setConfig(GetFullConfig(new_config))

        vis.add("arm_l_lpos",coordinates.Point(Local2WorldPos(arm_l_link, arm_l_localpos)))
        vis.add("arm_r_lpos",coordinates.Point(Local2WorldPos(arm_r_link, arm_r_localpos)))
        vis.add("leg_l_lpos",coordinates.Point(Local2WorldPos(leg_l_link, leg_l_localpos)))
        vis.add("leg_r_lpos",coordinates.Point(Local2WorldPos(leg_r_link, leg_r_localpos)))
        

        testPoint = Local2WorldPos(leg_r_link,leg_r_localpos)
        testPoint[0] += CM2M(10)                                 #put testpoint x cm in front of l_leg lpos
        vis.add("TestPoint",coordinates.Point(testPoint))

        #this updates the coordinates module
        coordinates.updateFromWorld()
        
        vis.unlock()

        print("##__DEBUG__##")
        print("mini config:     " + str(GetTrimmedConfig(mini.getConfig())))
        print("Angle:           " + str(joint_angle))
        print("Joint;           " + str(joint))
        print("iteration:       " + str(iteration))
        print("##############")

        if movement == True:
            joint_angle += 1

        if joint_angle > max_angle:
            joint       +=1
            joint_angle = 0

        if joint >= 16:
            joint       = 0
            joint_angle = 0

        iteration       += 1        
        time.sleep(sleepTime)

    # Terminate smoothly
    vis.kill()