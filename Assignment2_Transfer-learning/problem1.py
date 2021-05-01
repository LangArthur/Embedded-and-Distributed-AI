#!/usr/bin/env python3
#
# Created on Sat May 01 2021
#
# Arthur Lang
# problem1.py
#

import os
import tensorflow

from src.Model import Model

def checkGPU():
    if tensorflow.test.gpu_device_name():
        print('\033[94mGPU found\033[0m')
    else:
        print('\033[94mNo GPU found\033[0m')

def main():
    checkGPU()
    model = Model()
    return 0

if __name__ == '__main__':
    main()