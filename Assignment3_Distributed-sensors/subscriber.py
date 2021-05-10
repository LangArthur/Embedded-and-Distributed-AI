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

QUDT11 = Namespace("http://qudt.org/1.1/schema/qudt#")
QUDTU11 = Namespace("http://qudt.org/1.1/vocab/unit#")
CDT = Namespace("http://w3id.org/lindt/custom_datatypes#")
BASE = Namespace("http://example.org/data/") #TODO set this as a base

class Subscriber():

    def __init__(self):
        self.client = mqtt.Client("Subscriber") # mqtt client
        self.client.on_message = self.msgCallBack
        self.channel = "teds20/group07/pressure"
        self.timeout = 30 # time of inactivity in second before shutdown
        self.lastActivity = time.time() # time of the last activity
        self.mutex = Lock()
        self.isRunning = False
        self.graph = Graph() # rdf graph
        self.initGraph()
        self.nbrMsg = 0 # message counter
        self.lastObsId = 1 # id for observations

    # @method setGraphNamespace
    # set all the namespace in the graph.
    def setGraphNamespace(self):
        self.graph.base = BASE
        self.graph.bind('rdf', RDF)
        self.graph.bind('rdfs', RDFS)
        self.graph.bind('xsd', XSD)
        self.graph.bind('sosa', SOSA)
        self.graph.bind('qudt-1-1', QUDT11)
        self.graph.bind('qudt-unit-1-1', QUDTU11)
        self.graph.bind('cdt', CDT)

    # @method setGraphType
    # add all the used types to the graph.
    def setGraphType(self):
        # add earthAtmosphere
        self.earthAtmosphere = URIRef('earthAtmosphere')
        self.graph.add((self.earthAtmosphere, RDF.type, SOSA.FeatureOfInterest))
        self.graph.add((self.earthAtmosphere, RDFS.label, Literal("Atmosphere of Earth", lang='en')))
        # add sensor
        self.sensor = URIRef('sensor/35-207306-844818-0/BMP282')
        self.graph.add((self.sensor, RDF.type, SOSA.Sensor))
        self.graph.add((self.sensor, RDFS.label, Literal("Bosch Sensortec BMP282", lang='en')))
        sensorObs = URIRef('sensor/35-207306-844818-0/BMP282/atmosphericPressure')
        self.graph.add((self.sensor, SOSA.observers, sensorObs))
        # add Iphone
        self.iphone = URIRef('iphone7/35-207306-844818-0')
        self.graph.add((self.iphone, RDF.type, SOSA.Platform))
        self.graph.add((self.iphone, RDFS.label, Literal("IPhone 7 - IMEI 35-207306-844818-0", lang='en')))
        self.graph.add((self.iphone, RDFS.comment, Literal("IPhone 7 - IMEI 35-207306-844818-0 - John Doe", lang='en')))
        self.graph.add((self.iphone, SOSA.hosts, self.sensor))

    # @method initGraph
    # init the graph
    def initGraph(self):
        self.setGraphNamespace() # set all different namespace
        self.setGraphType() # set all types

    # @method publishInGraph
    # add the observation into the graph.
    # @param value: value of the observation
    # @param time: time of the observation
    def publishInGraph(self, value, time):
        obs = URIRef('Observation/' + str(self.lastObsId))
        sensorObs = URIRef('sensor/35-207306-844818-0/BMP282/atmosphericPressure')
        self.graph.add((obs, RDF.type, SOSA.Observation))
        self.graph.add((obs, SOSA.observedProperty, sensorObs))
        self.graph.add((obs, SOSA.hasFeatureOfInterest, self.earthAtmosphere))
        self.graph.add((obs, SOSA.madeBySensor, self.sensor))
        self.graph.add((obs, SOSA.hasSimpleResult, Literal(value, datatype=CDT['ucum'])))
        self.graph.add((obs, SOSA.resultTime, Literal(time, datatype=XSD['dateTime'])))
        self.lastObsId += 1

    # @method msgCallBack
    # callback when a message is received
    def msgCallBack(self, client, userdata, message):
        self.mutex.acquire()
        self.nbrMsg += 1
        self.lastActivity = time.time()
        self.mutex.release()
        if (self.nbrMsg <= 10):
            [reading, dt] = message.payload.decode('utf-8').split('|')
            self.publishInGraph(reading, dt)

    # @method run
    # function to start the subscriber
    def run(self):
        try:
            self.client.connect(MQT_SERVER)
            self.client.loop_start()
            self.client.subscribe(self.channel, qos=2)
            self.isRunning = True
            print("Ready to listen.")
            while (self.isRunning):
                self.mutex.acquire()
                if (time.time() - self.lastActivity > self.timeout or self.nbrMsg >= 10):
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
        # save file
        self.graph.serialize(destination='pressure.ttl', format='turtle')

# @function subscrib
# main function who init and launch the subscriber
def subscrib():
    subscriber = Subscriber()
    subscriber.run()

if __name__ == "__main__":
    subscrib()