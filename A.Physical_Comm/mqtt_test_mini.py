#! /usr/bin/python3

import paho.mqtt.client as mqtt
import time

broker_address      = "localhost"
client_id           = "1"
topic_connection    = "mini/connection" 
topic_data          = "mini/data"



def on_message(client, userdata, message):
    if message.topic == topic_connection and message.payload.decode("utf-8") == "testing connection":
        print("message received     " , str(message.payload.decode("utf-8")))
        print("message topic=       " , message.topic)
        print("message qos=         " , message.qos)
        print("message retain flag= " , message.retain)
        client.publish(topic_connection,"OK")

print("creating new instance")
client = mqtt.Client(client_id)       #create new instance
client.on_message=on_message    #attach function to callback
print("connecting to broker")
client.connect(broker_address)  #connect to broker
client.loop_start()             #start the loop
print("Subscribing to topic",topic_connection)
client.subscribe(topic_connection)
time.sleep(200) # wait
client.loop_stop() #stop the loop