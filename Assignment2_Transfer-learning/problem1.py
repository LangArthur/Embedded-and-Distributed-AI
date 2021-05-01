#!/usr/bin/env python3
#
# Created on Sat May 01 2021
#
# Arthur Lang
# problem1.py
#

import os

import tensorflow
from tensorflow import keras

def buildModel():
    model = keras.Sequential([
        keras.Input(shape=(25, 25)), # need to be change depending on the dataset
        keras.layers.Dense(3, activation="relu")
    ])
    return model

def preTraining():
    pass

def transferLearning():
    pass

# if we have the time to
def fineTuning():
    pass

def checkGPU():
    if tensorflow.test.gpu_device_name():
        print('GPU found')
    else:
        print('No GPU found')

def main():
    checkGPU()
    return 0

if __name__ == '__main__':
    main()