# smartCane

This is our project as a part of HackPrinceton Spring '25.

## Inspiration
We wanted to use our knowledge to build something that tries to solve a problem, is impactful, and has potential to be upscaled.

## What it does
Our smart cane integrates two key features to assist users: 
- Object Detection: Using a camera, the cane detects objects in the user’s surroundings through YOLO (You Only Look Once) object detection model trained on a dataset including pedestrians, bicycles, cars, etc. It then provides real-time audio feedback, describing the surroundings using the detected objects. 
- Haptic Feedback: Proximity sensors trigger vibrations in the handle to alert users when they are approaching an obstacle, providing haptic feedback to guide them in real-time. The vibration intensity depends on distance to obstacle.
These features work together to make navigation smoother, safer, and more intuitive for visually impaired individuals.

## How we built it
- Camera & Object Detection: A lightweight camera mounted on the cane feeds an image stream into a YOLO object detection model. We fine-tuned the model to recognize common obstacles and provide real-time descriptions using text-to-speech (TTS) technology.
- Proximity Sensors & Haptic Feedback: Ultrasonic sensors placed on the front of the cane detect objects within a certain distance. The data is sent to the Raspberry Pi, which triggers vibration motors embedded in the cane’s handle when objects get too close.
- Raspberry Pi: We used an embedded system to handle sensor data processing and control the camera, TTS system, and haptic actuators. It also hosts the client which does the computer vision work, while streaming the video feed to the server which handles the YOLO object detection. This was achieved using python's websockets.

## What's next for us
- Conducting deeper research to gather information on the specific needs of our target users. 
- In terms of hardware, we plan on adding more ultrasonic sensors for more detailed/fine grained haptic feedback. Additionally we would like to incorporate a GPS tracker onto the cane to leverage google maps API for a more detailed description of road and street networks, particularly crosswalks and junctions.
- In terms of software, we would like to add features such as voice control and a conversation AI model for a more interactive navigation experience. We would also add specific software modes based on user requirements.

## About the code
- ```websocketServer.py``` will be running on a machine with enough computational capability to run YOLOv5. It recieves a stream of images from the client on which it performs object detection, and returns a description of the objects present in the scene.
- ```websocketClient.py``` runs on the Raspberry Pi on the cane. It interfaces with the camera and OpenCV to record the video, interact with the server, and use Text to Speech technology to speak out auditory descriptions of what the camera sees.
- ```sensor_suite.py``` utilizes the Raspberry Pi's GPIO pins to interface with the sensors and motors, providing haptic feedback based on proximity to obstacles.
