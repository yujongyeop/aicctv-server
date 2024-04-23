from threading import Thread
from flask import Flask, Response, request
from ultralytics import YOLO
from PIL import Image
import cv2

from models.yolo8 import Yolov8

app = Flask(__name__)

model = Yolov8()



@app.route('/')
def index():
    return 'Hello!'


@app.route('/model/', methods=["GET","POST"])
def prediction():
    if request.method=="GET":
        streamURL = request.args.get('streamURL','rtsp://210.99.70.120:1935/live/cctv001.stream')
        results = model.model.predict(streamURL, stream=True,verbose=True,)
        for frame in results:
            frame = frame.plot()
            jpeg_image = cv2.imencode('.jpg', frame)[1].tobytes()
            res = Response()
            res
            return Response(jpeg_image, mimetype='multipart/x-mixed-replace; boundary=frame')
    elif request.method=="POST":
        return "POST"
    else:
        return "404"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1820, debug=True)