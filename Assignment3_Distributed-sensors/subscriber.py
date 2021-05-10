#!/usr/bin/env python3
#
# Created on Mon May 10 2021
#
# Arthur Lang
# subscriber.py
#

import paho.mqtt.client as mqtt
import sys
import time
import rdflib
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME

from threading import Lock

MQT_SERVER = "test.mosquitto.org"

class Subscriber():

    def __init__(self):
        self.client = mqtt.Client("Subscriber")
        self.client.on_message = self.msgCallBack
        self.channel = "teds20/group07/pressure"
        self.timeout = 300
        self.lastActivity = time.time()
        self.mutex = Lock()
        self.isRunning = False
        self.graph = Graph()
        self.initGraph()

    def initGraph(self):
        self.graph.bind('rdf', RDF)
        self.graph.bind('rdfs', RDFS)
        self.graph.bind('xsd', XSD)
        self.graph.bind('sosa', SOSA)
        print(self.graph.serialize(format='ttl').decode('u8'))

    def msgCallBack(self, client, userdata, message):
        self.mutex.acquire()
        self.lastActivity = time.time()
        self.mutex.release()
        print(f"\nmessage payload: {message.payload.decode('utf-8')}")
        print(f"message topic: {message.topic}")
        print(f"message qos: {message.qos}")
        print(f"message retain flag: {message.retain}")

    def run(self):
        try:
            self.client.connect(MQT_SERVER)
            self.client.loop_start()
            self.client.subscribe(self.channel, qos=2)
            self.isRunning = True
            print("Ready to listen.")
            while (self.isRunning):
                self.mutex.acquire()
                if (time.time() - self.lastActivity > self.timeout):
                    self.isRunning = False
                self.mutex.release()
                time.sleep(0.1) # set execution rate to avoid too many loop execution
            time.sleep(4)
            self.client.unsubscribe(self.channel)
            self.client.loop_stop()
            self.client.disconnect()
            print("Disconnected")


        except Exception as err:
            print("An error occured: {}".format(err), file=sys.stderr)

def subscrib():
    subscriber = Subscriber()
    subscriber.run()

if __name__ == "__main__":
    subscrib()