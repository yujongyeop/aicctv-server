from datetime import datetime
from subprocess import PIPE, Popen
import sys
import time
import cv2
import numpy
from ultralytics import YOLO
import os
class Yolov8:
    modelPath = ''
    model = '' 

    def __init__(self, modelPath = 'models/yolov8x.pt'):
        if self.modelPath == modelPath:
            print('Model: Yolov8x Selected!')
        else:
            print('Model: %s Selected', modelPath)
        self.model = YOLO(modelPath)

    def test(self):
        self.model('https://ultralytics.com/images/bus.jpg')

    def predictVideo(self, url):
        print('Start predict')

        # ffmpeg 실행 명령
        # ffmpeg_cli = 'ffmpeg -f rawvideo -pix_fmt bgr24 -r 20 -video_size 640x480 -i - -b:v 4000k -c:v mpeg4 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream'
        # ffmpeg_cli = 'ffmpeg -f rawvideo -pix_fmt bgr24 -r 20 -c:v libx264 -video_size 640x480 -i - -b:v 4000k -f flv rtmp://localhost:1935/live/test'
        
        # ffmpeg pipeline 생성
        # ffmpeg = Popen(ffmpeg_cli.split(), stdin=PIPE, stderr=PIPE ,shell=True)
        
        # YOLO Predict 설정 및 실행
        results = self.model.predict(
            url, # 영상 위치
            save=True, # 추론 결과 저장 여부(Default: False)
            device=0, # 연산 장치(Default: None[cpu]) 
            show=True, # 추론 결과(영상) 시각화(Default: False)
            stream=True, # 스트리밍 기능(Default: False) 
            verbose=False, # 추론 결과 반환(Default: True)
            save_txt=True, # 추론 결과 Text 저장(Default: False)
            )
        
        # 스트리밍 처리(Stream 옵션 활성화 시 사용)
        for frame in results: 
            processed_frame = frame.plot()  # 프레임 단위로 추론 결과 이미지를 가져옴
            # ffmpeg.stdin.write(processed_frame) # 결과 이미지를 pipeline을 통해 FFMPEG로 전달
        
        # pipeline 제거
        # ffmpeg.kill()
        print('Ended predict')

    def predictImage(self, url):
        print('Start Image predict')
        self.model.predict(url,save=True, show=True, line_width=10,show_labels=False)


    def predictWebCam(self, camIndex = 0):
        '''
        웹캠을 통한 객체 인식
        '''
        print('Start WebCam predict')
        # Camera 연결(기본값: 0)
        cap = cv2.VideoCapture(camIndex)
        
        # 카메라 설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        fps = 30
        cap.set(cv2.CAP_PROP_FPS, fps)
        w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height

        # 파일 저장 설정
        fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 비디오 코덱 방식
        file_name_format = "{:s}-{:%d-%m-%Y %H:%M-%S}.{:s}"
        PREFIX = 'Cam{camIndex}'
        EXTENSION = 'mp4'
        
        # ffmpeg pipeline 구축
        ffmpeg_cli = 'ffmpeg -f rawvideo -pix_fmt bgr24 -r 30 -video_size 640x480  -i - -b:v 4000k -c:v mpeg4 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/model/stream'
        ffmpeg = Popen(ffmpeg_cli.split() , stdin=PIPE, shell=True)
        
        while cap.isOpened():
            # 비디오 파일명 설정
            date = datetime.now()
            file_name = file_name_format.format(PREFIX,date,EXTENSION)
            out = cv2.VideoWriter('CAM/'+file_name, fourcc, 30, (w,h))
            
            #Save Video
            if not (out.isOpened()):
                print("File isn't opend!!")
                cap.release()
                sys.exit()

            # Read a frame from the video
            start_time = time.time()
            while(time.time() - start_time)<60:
                success, frame = cap.read()
                if success: 
                    results = self.model(frame,device=0,)
                    image = numpy.fromstring( results, dtype='uint8')
                    image = image.reshape((480,640,3)) 
                    ffmpeg.stdin.write(image)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    # Break the loop if the end of the video is reached
                    break

            out.release()
        cap.release()