#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import subprocess

broker_address      = "0.0.0.0"
client_id           = "2"
topic_connection    = "mini/connection" 
topic_data          = "mini/data"

counter = 0

output = subprocess.check_output(['sudo', 'iwgetid'])
print("==================================")
if (str(output).find("Robotis_Mini")):
    print("Connected to Robotis Mini Hotspot!")
    broker_address      = "192.168.50.5"
    
elif (str(output).find("LdL")):
    print("Connected to LdL Wifi!")
    broker_address      = "192.168.1.15"
else:
    print("Connected to unknown Wifi!")
    print("Aborting script...")
print("==================================")

if broker_address != "0.0.0.0":
    print("creating new instance")
    client = mqtt.Client(client_id)       #create new instance
    print("connecting to broker")
    client.connect(broker_address)  #connect to broker

    while True:
        output = "testing connection"
        print("Publishing '", output, "' to topic",topic_connection)
        client.publish(topic_connection,output)
        counter += 1
        time.sleep(0.1) # wait