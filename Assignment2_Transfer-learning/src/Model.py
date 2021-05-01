#!/usr/bin/env python3
#
# Created on Sat May 01 2021
#
# Arthur Lang
# Model.py
#

import tensorflow
import tensorflow_hub as hub
from tensorflow import keras

class Model:

    def __init__(self):
        self.inputShape = [None, 224, 224, 3]
        self.model = keras.Sequential([
            hub.KerasLayer("https://tfhub.dev/google/imagenet/resnet_v2_50/classification/5")
        ])
        self.model.build(self.inputShape)

    def preTraining(self):
        pass

    def transferLearning(self):
        pass

    # if we have the time to
    def fineTuning(self):
        pass
