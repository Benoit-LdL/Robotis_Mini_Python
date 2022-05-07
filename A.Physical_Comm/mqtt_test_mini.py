#! /usr/bin/python3

import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

broker_address="localhost"
print("creating new instance")
client = mqtt.Client("1")       #create new instance
client.on_message=on_message    #attach function to callback
print("connecting to broker")
client.connect(broker_address)  #connect to broker
client.loop_start()             #start the loop
print("Subscribing to topic","mini/test")
client.subscribe("/mini/test")
time.sleep(200) # wait
client.loop_stop() #stop the loop