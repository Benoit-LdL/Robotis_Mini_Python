#! /usr/bin/python3

import paho.mqtt.client as mqtt
import time

broker_address      = "localhost"
client_id           = "1"

MQTT_TOPIC = ["mini/config",
                "mini/data",
                "mini/out"]

MQTT_SUBS = []
MQTT_SUBS.append((MQTT_TOPIC[0],0))
MQTT_SUBS.append((MQTT_TOPIC[1],0))



def on_message(client, userdata, message):
    # print("message topic: " , message.topic)
    
    if message.topic == MQTT_TOPIC[0]:       # message on mini/config
        print("Topic:", message.topic, "| message: ", str(message.payload.decode("utf-8")))
        print("Publishing on topic " , str(MQTT_TOPIC[2]))
        client.publish(MQTT_TOPIC[2],"OK")

    elif message.topic == MQTT_TOPIC[1]:
        print("Topic:", message.topic, "| message: ", str(message.payload.decode("utf-8")))


print("creating new instance")
client = mqtt.Client(client_id)                 #create new instance
client.on_message=on_message                    #attach function to callback
print("connecting to broker")
client.connect(broker_address)                  #connect to broker
client.loop_start()                             #start the loop
print("Subscribing to topics")
client.subscribe(MQTT_SUBS)
time.sleep(200)                                 # wait
client.loop_stop()                              #stop the loop