from models.yolo8 import Yolov8

# Safe: Instantiating a single model inside each thread
from threading import Thread
modal = Yolov8()
modal.predictVideo('list.streams')