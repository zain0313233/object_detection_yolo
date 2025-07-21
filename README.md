# object_detection_yolo
A Object Detection Model In Python Detect real-time objects (like people, cars, etc.) using webcam
# 🧠 Real-Time Object Detection App with YOLOv5

This project uses **YOLOv5** (You Only Look Once) with **OpenCV** and **PyTorch** to perform real-time object detection on webcam/video feed. It can detect multiple objects like people, cars, animals, and more — using pre-trained models on the COCO dataset.

## 📸 Demo

![demo](https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg)

---

## 🚀 Features

- 🔍 Real-time object detection from webcam
- 🧠 Uses pre-trained YOLOv5 model (no training required)
- 🎯 Detects 80 common object classes (COCO dataset)
- 🧰 Draws bounding boxes and class labels
- 💾 Save detection results as images or video (optional)

---

## 📦 Technologies Used

- Python 3.8+
- [YOLOv5](https://github.com/ultralytics/yolov5)
- OpenCV
- PyTorch
- Numpy
- COCO Dataset

---

## 🔧 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
## 🔧 Download Yolo files must needed for detection
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names" -OutFile "coco.names"
Invoke-WebRequest -Uri "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights" -OutFile "yolov4.weights"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg" -OutFile "yolov4.cfg"