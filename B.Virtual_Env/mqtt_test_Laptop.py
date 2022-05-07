#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

broker_address="192.168.1.15"
print("creating new instance")
client = mqtt.Client("2")       #create new instance
print("connecting to broker")
client.connect(broker_address)  #connect to broker

while True:
    print("Publishing message to topic","mini/test")
    client.publish("/mini/test","testing connection")
    time.sleep(0.5) # wait