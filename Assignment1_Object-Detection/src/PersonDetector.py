#
# Created on Mon Apr 19 2021
#
# Arthur Lang
# PersonDetector.py
#

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class PersonDetector():

    def __init__(self, weight, config, classes, image):
        self.image= plt.imread(image)
        self.Width = self.image.shape[1]
        self.Height = self.image.shape[0]
        self.model = cv2.dnn.readNet(weight, config=config)
        self.classes = None
        with open('darknet/coco.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def get_prediction(self):
        self.model.setInput(cv2.dnn.blobFromImage(self.image, 0.00392, (416,416), (0,0,0), True, crop=False))
        layer_names = self.model.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]
        outs = self.model.forward(output_layers)
        return outs

    def draw_boxes(self, outs):

        class_ids = []
        confidences = []
        boxes = []

        #create bounding box 
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.1:
                    center_x = int(detection[0] * self.Width)
                    center_y = int(detection[1] * self.Height)
                    w = int(detection[2] * self.Width)
                    h = int(detection[3] * self.Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])


        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        return indices, boxes, class_ids

    def countPeople(self):
        outs = self.get_prediction()
        indices, boxes, class_ids,  = self.draw_boxes( outs)
        nrOfPeople=0
        for i in indices:
            i = i[0]
            box = boxes[i]
            if class_ids[i]==0:
                label = str(self.classes[0]) 
                cv2.rectangle(self.image, (round(box[0]),round(box[1])), (round(box[0]+box[2]),round(box[1]+box[3])), (0, 0, 0), 2)
                cv2.putText(self.image, label, (round(box[0])-10,round(box[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                nrOfPeople+=1     
        plt.imshow(self.image)
        plt.show()
        print('There are {} people in the image'.format(nrOfPeople))
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