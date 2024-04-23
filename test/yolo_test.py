import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.yolo8 import Yolov8
modal = Yolov8()
modal.predictVideo('model_test._3minmp4.mp4')