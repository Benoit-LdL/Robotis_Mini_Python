#!/usr/bin/env python3

from klampt import *
from klampt import IKObjective, IKSolver, vis, math
from klampt.model import coordinates, ik
from klampt.math import so3

import time, math

from numpy import angle, full

#   see gpu usage in cli:
#   watch -n 1 nvidia-smi

############################################################################################

#implementation = 1      #No robot movement             | IKSUCCESS=N.A
implementation = 1.1    #No max deviation & constraints| IKSUCCESS=true
#implementation = 1.2    #Max deviation                 | IKSUCCESS=true
#implementation = 1.3    #Max deviation & constraints   | IKSUCCESS=false
#implementation = 2      #using IKSOLVER & constraints  | IKSUCCESS=true

############################################################################################

###################################################
##############__SETTINGS__##############
worldFile   = "world.xml"
sleepTime   = 0.01
show_labels = False
max_angle   = 90
movement    = False
footAngle   = 90

##############__FUNCTIONS & METHODS__############## 
def CM2M(cm):                                   # Convert centimeters to meters (klampt coords are in meter)
    return cm/100.0

def MM2M(mm):                                   # Convert milimeters to meters (klampt coords are in meter)
    return mm/1000.0  


########################################
#               link number |   body part |     trimmed link number | servo ID |    Min Max servo angle
mini_links = [  11,             # neck          0                       0           -90 90
                
                15,             # l_hip         1                       8           -45 90      ##############__Mini Link Numbers__##############
                19,             # l_thigh       2                       10          -xx xx      38  l_shoulder_link                     86  r_shoulder_link
                23,             # l_knee        3                       12          -xx xx      41  l_biceps_link                       89  r_biceps_link
                27,             # l_ankle       4                       14          -xx xx      45  l_elbow_link                        93  r_elbow_link
                31,             # l_foot        5                       16          -xx xx    

                38,             # l_shoulder    6                       2           -90 90                  15  l_hip_link          63  r_hip_link
                41,             # l_biceps      7                       4           -90 90                  19  l_thigh_link        67  r_thigh_link
                45,             # l_elbow       8                       6           -90 90                  23  l_knee_link         71  r_knee_link
                                #                                                                           27  l_ankle_link        75  r_ankle_link
                63,             # r_hip         9                       7           -45 90                  31  l_foot_link         79  r_foot_link
                67,             # r_thigh       10                      9           -xx xx
                71,             # r_knee        11                      11          -xx xx
                75,             # r_ankle       12                      13          -xx xx
                79,             # r_foot        13                      15          -xx xx

                86,             # r_shoulder    14                      1           -90 90
                89,             # r_biceps      15                      3           -xx xx
                93]             # r_elbow       16                      5           -xx xx

mini_link_neck = 11
mini_links_l_arm = [38, 41, 45]         # Last element is end effector
mini_links_r_arm = [86, 89, 93]         # Last element is end effector
mini_links_l_leg = [15, 19, 23, 27, 31] # Last element is end effector
mini_links_r_leg = [63, 67, 71, 75, 79] # Last element is end effector

neck_localpos   = [0,           0,          0]          # end effector local position origin offset
arm_l_localpos  = [0,           -MM2M(75),  0]          # end effector local position origin offset
arm_r_localpos  = [0,           -MM2M(75),  0]          # end effector local position origin offset
leg_l_localpos  = [-MM2M(30),   -MM2M(9),   MM2M(30)]   # end effector local position origin offset
leg_r_localpos  = [MM2M(30),    -MM2M(9),   MM2M(30)]   # end effector local position origin offset

#################################################


##############__FUNCTIONS & METHODS__##############                            

def GetTrimmedConfig(full_config):              # Convert the full config to a trimmed version with only moving links
    full_config = mini.getConfig()
    trimmed_config = []
    for x in range(0,16):
        trimmed_config.append(full_config[mini_links[x]])
    return trimmed_config

def GetFullConfig(trimmed_config):              # Converted config containing moving links to the complete config
    full_config = [0] * mini.numLinks()
    for x in range(0,len(trimmed_config)):
        full_config[mini_links[x]] = trimmed_config[x]
    return full_config

def solve_ik(robotlink,localpos,worldpos):

    linkindex = robotlink.index
    robot = robotlink.robot()
    maxIters = 100
    tol = 1e-3 #1e-3
    restarts = 100
    maxDev = 50
    IKSucces = False

    (R,t) = robotlink.getTransform() 
    (axis,angle) = so3.axis_angle(R)
    
    ######################################
    ## Implementation 1: No robot movement
    ######################################
    if (implementation == 1):
        robot.setConfig(robot.setConfig([0]*robot.numLinks()))
        (R,t) = robotlink.getTransform()
        print(R)

    #######################################
    ## Implementation 1.1: No max deviation
    #######################################
    if (implementation == 1.1):
        print("===========================================================")
        print("__Implementation 1.1__")
        obj = ik.objective(robotlink,local=localpos,world=worldpos)
        obj2 = ik.objective(robotlink,R=so3.from_axis_angle(([0,1,0],(footAngle*(math.pi/180)))),t=t)   # [0,1,0] choose axis | toolAngle is the angle in degrees being converted to radians
        s = ik.solver([obj,obj2])
        print("Active DOFs:         " , str(s.getActiveDofs()))
        print("Setting active DOFs to right leg...")
        s.setActiveDofs(mini_links_r_leg)
        print("New active DOFs:     " , str(s.getActiveDofs()))
        print("===========================================================")
        # s.setJointLimits([],[])
        s.setMaxIters = maxIters
        s.setTolerance = tol
        IKSucces = s.solve()

    ####################################
    ## Implementation 1.2: Max deviation
    ####################################
    if (implementation == 1.2):
        obj = ik.objective(robotlink,local=localpos,world=worldpos)
        IKSucces = ik.solve_nearby(obj,maxDev,maxIters,tol,numRestarts=restarts)

    ##################################################
    ## Implementation 1.3: Max deviation & constraints
    ##################################################
    if (implementation == 1.3):
        obj = ik.objective(robotlink,local=localpos,world=worldpos)
        IKSucces = ik.solve_nearby(obj,maxDev,maxIters,tol)


    ###################################
    ## Implementation 2: using IKSOLVER & constraints
    ###################################
    if (implementation == 2):
        obj = coordinates.ik_objective(coordinates.getPoint("ik-constraint-local"),coordinates.getPoint("ik-constraint-world"))
        s = IKSolver(robot)
        s.add(obj)

        s.setMaxIters = maxIters
        s.setTolerance = tol
        IKSucces = s.solve()

    #################
    ## Debug & Output
    #################
    print()
    print("___________________")
    print("IK succes: " + str(IKSucces))
    #print("IK residual: " + str(s.getResidual()))
    #print("IK #iters: " + str(s.lastSolveIters()))
    #print("IK jacobian: " + str(s.getJacobian()))
    print("robot config: "  + str(robot.getConfig()))
    print("angle: "+ str(angle*(180/math.pi)))
    print("___________________")
    print()
    return robot.getConfig()



if __name__ == "__main__" :
    world = WorldModel()
    res = world.readFile(worldFile)
    if not res: RuntimeError("Unable to load world file")

    mini = world.robot(0)

    arm_l_linkIndex = mini_links_l_arm[len(mini_links_l_arm)-1]
    arm_r_linkIndex = mini_links_r_arm[len(mini_links_r_arm)-1]
    leg_l_linkIndex = mini_links_l_leg[len(mini_links_l_leg)-1]
    leg_r_linkIndex = mini_links_r_leg[len(mini_links_r_leg)-1]

    neck_link   = mini.link(mini_link_neck) 
    arm_l_link  = mini.link(arm_l_linkIndex)
    arm_r_link  = mini.link(arm_r_linkIndex)
    leg_l_link  = mini.link(leg_l_linkIndex)
    leg_r_link  = mini.link(leg_r_linkIndex)
    

    coordinates.setWorldModel(world)

    vis.add("world",world)
    
    if (show_labels):
        vis.add("coordinates", coordinates.manager())
    vis.show()
    iteration   = 0
    joint_angle = 0.0
    joint       = 16
    while vis.shown():
        vis.lock()
        
        new_config = [0] * mini.numDrivers()
        new_config[joint] = joint_angle*(math.pi/180)
        mini.setConfig(GetFullConfig(new_config))

        # Inverse Kinematics
        goalpoint = [0,0,0]
        goalpoint[0],goalpoint[1],goalpoint[2] = [CM2M(8),CM2M(-4),CM2M(4)]
        q = solve_ik(leg_r_link,leg_r_localpos,goalpoint)
        mini.setConfig(q)
        vis.add("GOAL",coordinates.Point(goalpoint))

        # vis.add("neck_lpos",coordinates.Point(neck_link.getWorldPosition(neck_localpos)))
        vis.add("arm_l_lpos",coordinates.Point(arm_l_link.getWorldPosition(arm_l_localpos)))
        vis.add("arm_r_lpos",coordinates.Point(arm_r_link.getWorldPosition(arm_r_localpos)))
        vis.add("leg_l_lpos",coordinates.Point(leg_l_link.getWorldPosition(leg_l_localpos)))
        vis.add("leg_r_lpos",coordinates.Point(leg_r_link.getWorldPosition(leg_r_localpos)))
        

        testPoint = leg_r_link.getWorldPosition(leg_r_localpos)
        testPoint[0] += CM2M(10)                                 #put testpoint x cm in front of l_leg lpos
        vis.add("TestPoint",coordinates.Point(testPoint))

        #this updates the coordinates module
        coordinates.updateFromWorld()
        
        vis.unlock()

        print("##__DEBUG__##")
        print("mini config:     " + str(GetTrimmedConfig(mini.getConfig())))
        #print("q:               " + str(q))
        # print("# joints:        " + str(mini.numLinks()))
        # print("# Drivers:       " + str(mini.numDrivers()))
        print("Angle:           " + str(joint_angle))
        print("Joint;           " + str(joint))
        print("iteration:       " + str(iteration))
        print("##############")

        if movement == True:
            joint_angle += 1

        if joint_angle > max_angle:
            #joint       +=1
            joint_angle = 0

        if joint > mini.numDrivers()-1:
            joint       = 0
            joint_angle = 0

        iteration       += 1        
        time.sleep(sleepTime)

    # Terminate smoothly
    vis.kill()