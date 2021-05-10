#!/usr/bin/env python3
#
# Created on Mon May 10 2021
#
# Arthur Lang
# publisher.py
#

import paho.mqtt.client as mqtt
import time
import sys
import numpy
import datetime

MQT_SERVER = "test.mosquitto.org"

def readSensorData():
    mu, sigma = 1200.00, 1.0
    reading = f'{round(numpy.random.normal(mu, sigma), 2):.2f}'        
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'
    return message

def publisher():
    client = mqtt.Client("Publisher")
    channel = "teds20/group07/pressure"

    try:
        client.connect(MQT_SERVER)
        client.loop_start()
        client.subscribe(channel, qos=2)
        print("Ready to publish.")
        # loop to send 10 messages
        for _ in range(10):
            message = readSensorData()
            print("Send: {}".format(message))
            client.publish(channel, message, qos=2)
            time.sleep(1)
        time.sleep(4)
        client.unsubscribe(channel)
        client.loop_stop()
        client.disconnect()
        print("Disconnected")
    except Exception as err:
        print("An error occured: {}".format(err), file=sys.stderr)
    return 0

if __name__ == "__main__":
    publisher()