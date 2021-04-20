#
# Created on Mon Apr 19 2021
#
# Arthur Lang
# PersonDetector.py
#

import sys
import cv2
import numpy as np

class PersonDetector():

    def __init__(self, weight, config, classes):
        self.model = cv2.dnn.readNet(weight, config=config)
        self.classes = None
        with open('darknet/coco.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def _getPrediction(self, img):
        self.model.setInput(cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0,0,0), True, crop=False))
        layer_names = self.model.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]
        outs = self.model.forward(output_layers)
        return outs

    def _getBoxes(self, outs, width, height):
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
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        return indices, boxes, class_ids

    def countPeople(self, imagePath):
        image = cv2.imread(imagePath)
        if image is None:
            print("Error: can't open the file.", file=sys.stderr)
            return 1
        outs = self._getPrediction(image)
        indices, boxes, class_ids,  = self._getBoxes(outs, image.shape[1], image.shape[0])
        nrOfPeople = 0
        for i in indices:
            i = i[0]
            box = boxes[i]
            if class_ids[i] == 0:
                label = str(self.classes[0]) 
                cv2.rectangle(image, (round(box[0]), round(box[1])), (round(box[0] + box[2]),round(box[1] + box[3])), (0, 0, 0), 2)
                cv2.putText(image, label, (round(box[0]) - 10, round(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                nrOfPeople += 1
        # cv2.namedWindow("People detection", cv2.WINDOW_NORMAL)
        cv2.imshow("People detection", image)
        print('There are {} people in the image'.format(nrOfPeople))
        cv2.waitKey()
        return 0