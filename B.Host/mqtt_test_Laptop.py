#!/usr/bin/env python3

from numpy import concatenate
import paho.mqtt.client as mqtt
import time
import subprocess

###############__DEFAULT_VALUES__###############

MQTT_BROKER                 = "0.0.0.0"
MQTT_BROKER_INTERNAL        = "192.168.1.15"
MQTT_BROKER_EXTERNAL        = "192.168.50.5"
CLIENT_ID                   = "2"
mqtt.Client.connected_flag  = False
MQTT_TOPIC = ["mini/config",
                "mini/data",
                "mini/out"]

MQTT_SUBS = []
MQTT_SUBS.append((MQTT_TOPIC[2],0))
wifi_name = str(subprocess.check_output(['sudo', 'iwgetid']))
WAITING_RESPONSE            = False

###############__FUNCTIONS__###############

def Check_wifi_name():
    global MQTT_BROKER
    print("==================================")
    if (wifi_name.find("Robotis_Mini") != -1):
        print("Connected to Robotis Mini Hotspot!")
        MQTT_BROKER      = MQTT_BROKER_EXTERNAL
        
    elif (wifi_name.find("LdL") != -1):
        print("Connected to LdL Wifi!")
        MQTT_BROKER      = MQTT_BROKER_INTERNAL
    else:
        print("Connected to unknown Wifi!")
        print("Aborting script...")
    print("==================================")

def Setup_client():
    print("creating client")
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = On_connect
    client.on_message = On_message  
    client.loop_start()
    print("connecting to broker: ",MQTT_BROKER)
    client.connect(MQTT_BROKER)
    return client

def On_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.connected_flag = True
    else:
        print("Bad connection Returned code=",rc)

def Wait_for_connection(client):
    while not client.connected_flag:
        print("wating for connection...")
        time.sleep(0.5)

def On_message(client, userdata, message):
    global WAITING_RESPONSE
    if message.topic == MQTT_TOPIC[2]:
        print("received message from ", message.topic , " : " , str(message.payload.decode("utf-8")))
        WAITING_RESPONSE = False

##########################################

counter = 0


if __name__ == "__main__":

    Check_wifi_name()
    
    #print("mqtt broker: " + MQTT_BROKER)

    if MQTT_BROKER != "0.0.0.0":
        
        client = Setup_client()

        Wait_for_connection(client)
        
        print("Subscribing to topics")
        client.subscribe(MQTT_SUBS)

        while True:
            testConfig = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            output = str(testConfig)
            # print("Publishing '", str(output), "' to topic",MQTT_TOPIC[0])
            WAITING_RESPONSE = True
            
            while WAITING_RESPONSE == True:
                print("Publishing...")
                client.publish(MQTT_TOPIC[0],output)
                print("waiting for a response...")
                time.sleep(0.1)
            
            output = "testing data topic"
            print("Publishing '", str(output), "' to topic",MQTT_TOPIC[1])
            client.publish(MQTT_TOPIC[1],output)

            # counter += 1
            time.sleep(0.1) # wait