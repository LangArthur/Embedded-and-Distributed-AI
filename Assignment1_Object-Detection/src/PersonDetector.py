#
# Created on Mon Apr 19 2021
#
# Arthur Lang
# PersonDetector.py
#

import sys
import cv2
import numpy as np

# @class PersonDetector
# a class that allow to detect persons
class PersonDetector():

    def __init__(self, weight, config, classes):
        # load model
        self.model = cv2.dnn.readNet(weight, config=config)
        # get classes detected by the loaded network
        self.classes = None
        with open('darknet/coco.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.detection = "person"

    # @method _getPrediction
    # @return all the object detected in the scene.
    def _getPrediction(self, img):
        self.model.setInput(cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0,0,0), True, crop=False))
        layer_names = self.model.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]
        outs = self.model.forward(output_layers)
        return outs

    # @method _getBoxes
    # compute position of boxes from detections
    # @param outs: list with all the detections
    # @param width: width of the image the detection was made on.
    # @param height: height of the image the detection was made on.
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

    # @method countPeople
    # count number of people on an image and display them
    # @param imagePath: path of the image with persons
    # @return number of people or -1 in case of error
    def countPeople(self, imagePath):
        # read picture
        image = cv2.imread(imagePath)
        if image is None:
            print("Error: can't open the image.", file=sys.stderr)
            return -1
        # predict
        outs = self._getPrediction(image)
        indices, boxes, class_ids,  = self._getBoxes(outs, image.shape[1], image.shape[0])
        nrOfPeople = 0
        for i in indices:
            i = i[0]
            box = boxes[i]
            if self.classes[class_ids[i]] == self.detection:
                label = str(self.detection)
                cv2.rectangle(image, (round(box[0]), round(box[1])), (round(box[0] + box[2]),round(box[1] + box[3])), (0, 0, 0), 2)
                cv2.putText(image, label, (round(box[0]) - 10, round(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                nrOfPeople += 1
        cv2.imshow("People detection", image)
        print('There {} {} {} in the image.'.format(("are" if nrOfPeople > 1 else "is"), nrOfPeople, self.detection + ("s" if nrOfPeople > 1 else "")))
        cv2.waitKey()
        return nrOfPeople