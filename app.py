from threading import Thread
from flask import Flask, Response, jsonify, request
from ultralytics import YOLO
from PIL import Image
import cv2

from models.yolo8 import Yolov8

app = Flask(__name__)

model = Yolov8('yolov8n.pt')

def modelPredict():
    streamURL = 'rtsp://210.99.70.120:1935/live/cctv001.stream'
    results = model.model.predict(streamURL, stream=True,verbose=True,)
    for frame in results:
        framePlot = frame.plot()
        jpeg_image = cv2.imencode('.jpg', framePlot)[1]
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(jpeg_image) + b'\r\n')


@app.route('/')
def index():
    return 'Hello!'

@app.route('/model/', methods=["GET","POST"])
def prediction():
    if request.method=="GET":
        return Response(modelPredict(), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif request.method=="POST":
        return "POST"
    else:
        return "404"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1820, debug=True)