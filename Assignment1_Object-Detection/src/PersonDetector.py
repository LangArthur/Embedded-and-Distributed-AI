#
# Created on Mon Apr 19 2021
#
# Arthur Lang
# PersonDetector.py
#

import cv2
import numpy

class PersonDetector():

    def __init__(self, weight, config, classes):
        self.model = cv2.dnn.readNet(weight, config=config)
        self.classes = []
        with open(classes, "r") as fd:
            self.classes = [line.strip() for line in fd]
        layerNames = self.model.getLayerNames()
        self.outputLayers = self.model.getUnconnectedOutLayers()
        # self.outputLayers = [layerNames[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]

    # def preprocess(self, img):
    #     return cv2.resize(img, None, fx=0.4, fy=0.4)

    def countPerson(self, img):
        # img = self.preprocess(img)
        blob = cv2.dnn.blobFromImage(img, 1, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.outputLayers)
        # class_ids = []
        # confidences = []
        # boxes = []

        # for out in outs:
        #     for detection in out:
        #         scores = detection[:5]
        #         ids = numpy.argmax(scores) 
        #         confidence = scores[ids]
        #         if (confidence > 0.1):
        #             center_x = int(detection[0] * img.shape[1])
        #             center_y = int(detection[1] * img.shape[0])
        #             w = int(detection[2] * img.shape[1])
        #             h = int(detection[3] * img.shape[0])
        #             x = int(center_x - w / 2)
        #             y = int(center_y - h / 2)
        #             class_ids.append(ids)
        #             confidences.append(float(confidence))
        #             boxes.append([x, y, w, h])

        # indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        # #check if is people detection
        # for i in indices:
        #     i = i[0]
        #     box = boxes[i]
        #     if class_ids[i]==0:
        #         label = str(self.classes[class_id]) 
        #         cv2.rectangle(img, (round(box[0]),round(box[1])), (round(box[0]+box[2]),round(box[1]+box[3])), (0, 0, 0), 2)
        #         cv2.putText(img, label, (round(box[0])-10,round(box[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # cv2.imshow("detection", img)
        # cv2.waitKey()
        return 0