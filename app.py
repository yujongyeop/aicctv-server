import base64
import threading
from flask import Flask, Response, json, render_template, request
from ultralytics import YOLO
from PIL import Image
import cv2

from models.yolo8 import Yolov8

app = Flask(__name__)

model = YOLO('yolov8x.pt')

realtime_img = ''
realtime_object= {}

def predictionProcessing():
    streamURL = 'rtsp://210.99.70.120:1935/live/cctv001.stream'
    results = model.predict(streamURL, device=0, stream=True,verbose=False,)
    for frame in results:
        framePlot = frame.plot()
        jpeg_image = cv2.imencode('.jpg', framePlot)[1]
        detectedClass = frame.boxes.cls.cpu().numpy().astype(int).tolist()
        global realtime_img, realtime_object
        realtime_img = jpeg_image.tobytes()
        realtime_object = detectedClass
        # yield (b'--frame\r\n' b'Content-Type: image/jpegr\\n\r\n'+ base64.b64encode(jpeg_image) + b'\r\n\r\nContent-Type: text/json\r\n\r\n'+ bytes(json.dumps({'classes':detectedClass}), 'utf-8') + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

def modelPredict():
    i= 0
    while True:
        print(i)
        i+=1 
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ realtime_img + b'\r\n')

def getClass():
    while True:
        yield (b'--data\r\n' b'Content-Type: application/json\r\n\r\n'+ bytes(json.dumps({'classes':realtime_object}), 'utf-8') + b'\r\n')

@app.route('/model/', methods=["GET","POST"])
def prediction():
    if request.method=="GET":
        return Response(modelPredict(),headers= {"connection":"Keep-Alive", "Access-Control-Allow-Origin":"http://soompyo.com:9999/model"}, mimetype='multipart/x-mixed-replace; boundary=frame',)
    elif request.method=="POST":
        print('POST Request')
        return "POST"
    else:
        print('Error Request')
        return "404"
    
@app.route('/getClass/', methods=["GET","POST"])
def getobject():
    if request.method=="GET":
        return Response(getClass(),headers= {"connection":"Keep-Alive", "Access-Control-Allow-Origin":"http://soompyo.com:9999/getClass"}, mimetype='multipart/x-mixed-replace; boundary=data',)
    elif request.method=="POST":
        print('POST Request')
        return "POST"
    else:
        print('Error Request')
        return "404"
    

if __name__ == "__main__":
    YOLOThread = threading.Thread(target= predictionProcessing)
    YOLOThread.start()
    appThread = threading.Thread(target=app.run, args=('0.0.0.0', '9999',))
    appThread.start()
    # app.run(host='0.0.0.0', port=9999, debug=True)