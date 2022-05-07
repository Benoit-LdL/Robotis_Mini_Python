#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

broker_address      = "192.168.1.15"
client_id           = "2"
topic_connection    = "mini/connection" 
topic_data          = "mini/data"

print("creating new instance")
client = mqtt.Client(client_id)       #create new instance
print("connecting to broker")
client.connect(broker_address)  #connect to broker

counter = 0

while True:
    output = "testing connection"
    print("Publishing '", output, "' to topic",topic_connection)
    client.publish(topic_connection,output)
    counter += 1
    time.sleep(0.1) # wait