# Webcam으로부터 받은 영상을 FFMPEG
import cv2
from subprocess import PIPE, Popen
from PIL import Image
import numpy


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width, ch = frame.shape
dimension = '{}x{}'.format(width, height)
f_format = 'bgr24' # remember OpenCV uses bgr format
fps = str(cap.get(cv2.CAP_PROP_FPS))
ffmpeg_cli = 'ffmpeg -f rawvideo -pix_fmt bgr24 -r 30 -video_size 640x480  -i - -b:v 4000k -c:v mpeg4 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/model/stream'

ffmpeg = Popen(ffmpeg_cli.split() , stdin=PIPE, shell=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    try:
        cv2.imshow('1',frame)
        image = numpy.fromstring(frame, dtype='uint8')
        image = image.reshape((480,640,3)) 
        ffmpeg.stdin.write(image)
        if cv2.waitKey(33) & 0xFF == ord("q"):
            break
    except (Exception):
        print('Excepted')
