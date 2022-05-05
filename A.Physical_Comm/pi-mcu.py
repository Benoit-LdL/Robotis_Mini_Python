#! /usr/bin/python3
import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)

counter = 0
output = ""
DEFAULT_SPEED = 10
#-----Data structure-----
#[action];[param1;param2;...]
#
#move;M motorId; P position; S speed    -> "move;S1;P180;S10"   = move servo 1 to position 180 at speed 10
#read;S servoId;                        -> "read;S2"            = read data from servo 2 and send back actual pos, voltage,...
#
#
#
#------------------------

#-----Functions and Methods-----
def WaitForArduino():
    wait = 1
    while (wait == 1):
        print("waiting for arduino...")
        input=str(ser.readline().decode()).rstrip()
        #print(input)
        if (input == '<Arduino is ready>'):
            wait = 0
            #print('correct')

def MoveMessage(id,pos,spd = DEFAULT_SPEED):
    return ('move' + ';'
        + str(id) +';'    # Motor ID
        + str(pos) + ';'  # Motor position
        + str(spd) + ';'  # Motor speed
        + '\n')

def ReadMessage(id):
    output = 'read' + ';' + str(id) + ';' + '\n'
    ser.write(output.encode())
    print("sending -> " + output + '\n')
    print('waiting...\n')
    cc=str(ser.readline())
    print('response: ' + cc + '\n')

#-----CODE-----

WaitForArduino()

while True:
    #ReadMessage(1);
    output=MoveMessage(1,counter,counter*2)
    ser.write(output.encode())
    print("sending -> " + output)

    counter+=1
    if (counter >= 1000):
        counter = 0;
    time.sleep(0.1)




################################
#--- data from Arduino ---
# cc=str(ser.readline())
# print(cc)
