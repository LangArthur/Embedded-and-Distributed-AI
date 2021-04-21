# Embedded-and-Distributed-AI
A repository for the course Embedded and Distributed AI.

## Installation

In each assignment folders, you can find a requirements.txt with all the needed dependencies. We recommand to use pip to install them.

```
pip install -r requirements.txt
```

For the assignment 2, we were not able to upload weights for the model. To do so, download the weights, config and names from Yolov3 and place them in a folder Assignment1_Object-Detection/darknet/ (to the teacher: we copied the weights from the workshop n°2. If it's not exaclty weights from Yolov3, can you warn us about the specificity of your weights?).

## Assignment 1: Object detection

this project is seperate in two differents problems

### problem 1: Picture matching

This projet match a picture (called template) into another one.

Pictures are given inside the repository, but you can create your own templates with -e flag.

### problem 2: Person detection

This project detect the number of person on a picture, specified in parameter of the program.

We provide different pictures to test the algorithm. The picture "too_many_persons.jpg" show the limitation of the algorithm: when peoples are too much hide or too far, the algorithm did not detect them.

## Bonus

In bonus, you can specify, in the constructor of the Detector (problem 2), the target you want to detect. We supplied a picture, 2persons-bicycle.jpg, on which you can change the detection and only detect bicyles:
```
detect = Detector("darknet/yolov3.weights", "darknet/yolov3.cfg", "darknet/coco.names", "bicycle")
```

or use the setter updateTarget("bicycle").

## Authors

* **Arthur LANG** - *Initial work* - [LangArthur](https://github.com/LangArthur)
* **Madalina Aldea** - *Initial work* - [MadalinaAldea](https://github.com/MadalinaAldea)