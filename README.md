# Embedded-and-Distributed-AI
A repository for the course Embedded and Distributed AI.

## Installation

In each assignment folders, you can find a requirements.txt with all the needed dependencies. We recommand to use pip to install them.

```
pip install -r requirements.txt
```

For the assignment 1, in the problem 2, we were not able to upload weights for the model, due to github size limitation. To make it work, download the weights, config and names from Yolov3 and place them in a folder Assignment1_Object-Detection/darknet/ (to the teacher: we copied the weights from the workshop n°2. If it's not exaclty weights from Yolov3, can you warn us about the specificity of your weights?).

## Assignment 1: Object detection

this project is seperate in two differents problems

### problem 1: Picture matching

This projet match a picture (called template) into another one.

Pictures are given inside the repository, but you can create your own templates with -e flag.

### problem 2: Person detection

This project detect the number of person on a picture, specified in parameter of the program.

We provide different pictures to test the algorithm. The picture "too_many_persons.jpg" show the limitation of the algorithm: when peoples are too much hide or too far, the algorithm did not detect them.

### Bonus

In bonus, you can specify, in the constructor of the Detector (problem 2), the target you want to detect. We supplied a picture, 2persons-bicycle.jpg, on which you can change the detection and only detect bicyles:
```
detect = Detector("darknet/yolov3.weights", "darknet/yolov3.cfg", "darknet/coco.names", "bicycle")
```

or use the setter updateTarget("bicycle").

## Assignment 2: Transfer Learning and Model Compression

This assignment uses transfer learning and the TFLite Converter/Interpreter to create a "traffic sign" classifier. The assignment is divided into 2 parts.

### Problem 1: Transfer Learning

In this problem, a headless pre-trained model from TensorFlow Hub is used for creating a classifier for German Traffic Sign Dataset. For this task, the first 6 classes from the dataset were used in order to reduce the complexity. The accuracy of the model on test dataset is 0.86.

Pre-trained model: "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/5"

### Problem 2: Model Compression

The model from the Problem 1 was converted into a TF Lite model. The sized of the model was reduced from 18.7 MB to 16 MB. The compressed model classifies a single image in 0.07 and has an accuracy of 85.08%.


In order to run the Google Colab notebook, the output folder which contains the train, test and validation dataset has to be unzipped and the path of the folder has to be specified in the parameters. The uncompressed model can be found in  "\Models\1620048460" and the TF lite model can be found in "\Models\model.tflite". The full path of this models has to be specified in the notebook also.



## Authors

* **Arthur LANG** - *Initial work* - [LangArthur](https://github.com/LangArthur)
* **Madalina Aldea** - *Initial work* - [MadalinaAldea](https://github.com/MadalinaAldea)
