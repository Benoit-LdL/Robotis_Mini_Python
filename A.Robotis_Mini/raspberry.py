#!/usr/bin/env python3
#===========================================================#
# Copy of DynamixelSDK/python/tests/protocol2_0/read_write.py
#===========================================================#
import os
import time
import sys, tty, termios
from dynamixel_sdk import * # Uses Dynamixel SDK library

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

#
# Voltage       = 8.40V
# Max Current   = 0.75A
#
########################################
# Body part | servo ID
# neck        -1

# r_shoulder  1
# r_biceps    3
# r_elbow     5

# l_shoulder  2
# l_biceps    4
# l_elbow     6

# r_hip       7
# r_thigh     9
# r_knee      11
# r_ankle     13
# r_foot      15

# l_hip       8
# l_thigh     10
# l_knee      12
# l_ankle     14
# l_foot      16 
#********* DYNAMIXEL Model definition *********
MY_DXL = 'XL320'                        # [WARNING] Operating Voltage : 7.4V
BAUDRATE                    = 1000000   # Default Baudrate of XL-320 is 1Mbps

ADDR_TORQUE_ENABLE          = 24
ADDR_LED                    = 25
ADDR_GOAL_POSITION          = 30
ADDR_SPEED                  = 32
ADDR_PRESENT_POSITION       = 37
ADDR_VOLTAGE                = 45
ADDR_TEMPERATURE            = 46

DXL_ZERO_POSITION           = 512       # all servo zero pos are half of limit : 1024/2
DXL_MIN_POS_DEC             = 0         # Refer to the CW Angle Limit of product eManual
DXL_MAX_POS_DEC             = 1023      # Refer to the CCW Angle Limit of product eManual
DXL_POS_THRESH_PERCENTAGE   = 5        # threshold of position accuracy of servos in %
DXL_POS_THRESHOLD           = 15  #round(DXL_MAX_POS_DEC/DXL_POS_THRESH_PERCENTAGE) 

DXL_MIN_POS_DEG             = -150
DXL_MAX_POS_DEG             = 150

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      =  5
DXL_ID_LIST                 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
DXL_ACTIVE_ID_LIST          = []
DEVICENAME                  = '/dev/serial0'# '/dev/ttyAMA0'      # '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

COLOR_OFF, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_PURPLE, COLOR_CYAN, COLOR_WHITE       = 0,1,2,3,4,5,6,7


index = 0

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)


##################__FUNCTIONS__##################

def ConvertSpeed(rpm):
    if rpm > 0:
        out = round(rpm / 0.111)    # range in joint mode is 0-1023 with 0.111 rpm/increment
    else:
        out = 0

    if out > DXL_MAX_POS_DEC:
        out = DXL_MAX_POS_DEC
    
    print("converted rpm: " , str(out))
    return out

def MapRange(input,from_min,from_max,to_min,to_max):
    return ((input - from_min) * (to_max - to_min) / (from_max - from_min) + to_min )

def ConvertDecimal2Angle(decimal):
    angle = round(MapRange(decimal,DXL_MIN_POS_DEC,DXL_MAX_POS_DEC,DXL_MIN_POS_DEG,DXL_MAX_POS_DEG),2)
    print("angle: " , str(angle))
    return angle

def getch():
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def BroadCastPing():
    global portHandler, DXL_ACTIVE_ID_LIST
    broadcast_ping_list, result = packetHandler.broadcastPing(portHandler)
    if result != COMM_SUCCESS:
        print("BroadCastPing: %s" % packetHandler.getTxRxResult(result))
    print("detected dynamixels:")
    for dxl_id in broadcast_ping_list:
        # print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, broadcast_ping_list.get(dxl_id)[0], broadcast_ping_list.get(dxl_id)[1]))
        DXL_ACTIVE_ID_LIST.append(dxl_id)
        # print("Active servos:   " , str(DXL_ACTIVE_ID_LIST))

def GetInactiveServos():
    global DXL_ID_LIST, DXL_ACTIVE_ID_LIST
    output = []
    for i in range(len(DXL_ID_LIST)):
        if DXL_ID_LIST[i] not in DXL_ACTIVE_ID_LIST:
            output.append(DXL_ID_LIST[i])  
    return output

def ReadData(id,address):
    global portHandler
    data, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, id, address)
    if dxl_comm_result != COMM_SUCCESS:
        print("ReadData: %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("ReadData: %s" % packetHandler.getRxPacketError(dxl_error))
    return data

def ReadBulk(id_list,adress):
    data = []
    for id in id_list:
        data.append(ReadData(id,adress))
    return data

def WriteData(id,address,data):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, address, data)
    if dxl_comm_result != COMM_SUCCESS:
        print("WriteData: %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("WriteData: %s" % packetHandler.getRxPacketError(dxl_error))

def WriteBulk(id_list,adress,data_list):
    for i in range(len(id_list)):
        WriteData(id_list[i],adress,data_list[i])

def MoveServo(id,position,rpm):
    rpm_to_dec          = round(rpm / 0.111)
    
    WriteData(DXL_ID,ADDR_SPEED, rpm_to_dec)
    WriteData(DXL_ID,ADDR_GOAL_POSITION,position)

    while True:     # Waiting until the servo has achieved the goal position with accuracy threshold in mind
        present_pos = ReadData(id,ADDR_PRESENT_POSITION)
        # print("present / goal: %d / %d" %(present_pos,position))
        if  present_pos <= position+DXL_POS_THRESHOLD and present_pos >= position-DXL_POS_THRESHOLD:
            break
        time.sleep(0.05)
        # print("waiting...")

#################################################


# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# # Enable Dynamixel Torque
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))
# else:
#     print("Dynamixel has been successfully connected")


BroadCastPing()

#Turn on led of servo 1
print("##############")
print("testing LED")
WriteBulk(DXL_ACTIVE_ID_LIST,ADDR_LED,[COLOR_WHITE] * len(DXL_ACTIVE_ID_LIST))
print("##############")

while len(DXL_ACTIVE_ID_LIST) > 1:

    #==========__Reading data__==========
    
    # voltage_list        = ReadBulk(DXL_ACTIVE_ID_LIST,ADDR_VOLTAGE)
    # temperature_list    = ReadBulk(DXL_ACTIVE_ID_LIST,ADDR_TEMPERATURE)
    # postion_list        = ReadBulk(DXL_ACTIVE_ID_LIST,ADDR_PRESENT_POSITION)
    
    # print("##__DEBUG__##")
    # print("# Active servos servos:  " , str(len(DXL_ACTIVE_ID_LIST)))
    # print("Offline servos:          " , str(GetInactiveServos()))
    # print("V:           " , str(voltage_list))
    # print("T:           " , str(temperature_list))
    # print("POS:         " , str(postion_list))
    # print("#############")
    # time.sleep(0.1)

    #==========__Writing data__==========

    MoveServo(DXL_ID,400,20)

    # print("extra sleep...")
    # time.sleep(1)

    MoveServo(DXL_ID,700,10)

    # print("extra sleep...")
    # time.sleep(1)

print("No servos connected, shutting down script...")

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
