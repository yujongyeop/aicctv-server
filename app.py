from flask import Flask
from ultralytics import YOLO
from PIL import Image
import cv2

from models.yolo8 import Yolov8

app = Flask(__name__)
model = Yolov8()
model.predictVideo('https://www.youtube.com/watch?v=cVvDE4qO-3E')

@app.route('/')
def index():
    return 'Hello!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1820, debug=True)