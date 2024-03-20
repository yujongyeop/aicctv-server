from datetime import datetime
import sys
import time
import cv2
from ultralytics import YOLO


class Yolov8:
    modelPath = 'models/yolov8n.pt'
    model = ''
    def __init__(self, modelPath = 'models/yolov8n.pt'):
        if self.modelPath == modelPath:
            print('Model: Yolov8n Selected!')
        else:
            print('Model: %s Selected', modelPath)
        self.model = YOLO(self.modelPath)

    def test(self):
        self.model('https://ultralytics.com/images/bus.jpg')

    def predictVideo(self, url):
        print('Start predict')
        result = self.model.predict(url, save=True,show=True)
        print(result)
        print('Ended predict')

    def predictImage(self, url):
        self.model.predict(url,save=True, show=True)
        print('Start Image predict')


    def predictWebCam(self, camIndex = 0):
        '''
        웹캠을 통한 객체 인식
        '''
        print('Start WebCam predict')
        # Camera 연결(기본값: 0)
        cap = cv2.VideoCapture(camIndex)
        # 카메라 프레임
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        cap.set(cv2.CAP_PROP_FPS, 60)
        #Set Video File Property
        videoFileName = 'output.mp4'
        w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        fps = cap.get(cv2.CAP_PROP_FPS) #frame per second
        fourcc = cv2.VideoWriter_fourcc(*'DIVX') #fourcc
        delay = round(1000/fps) #set interval between frame
        while cap.isOpened():
            # 파일명
            PREFIX = 'Cam'
            EXTENSION = 'mp4'
            file_name_format = "{:s}-{:%d-%m-%Y %H:%M-%S}.{:s}"
            date = datetime.now()
            today = time.strftime('%d-%m-%Y')
            file_name = file_name_format.format(PREFIX,date,EXTENSION)
            out = cv2.VideoWriter('CAM/'+file_name, fourcc, 30, (w,h))
            
            
            #Save Video
            if not (out.isOpened()):
                print("File isn't opend!!")
                cap.release()
                sys.exit()

            # Read a frame from the video
            start_time = time.time()
            i = 0
            while(time.time() - start_time)<10:
                i+=1
                success, frame = cap.read()
                if success: 
                    # Run YOLOv8 inference on the frame
                    results = self.model(frame,)
                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()
                    out.write(annotated_frame)
                    # Display the annotated frame
                    # cv2.imshow("WebCam Live Monitor", annotated_frame)
                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    # Break the loop if the end of the video is reached
                    break

            # Release the video capture object and close the display window
            out.release()
        cap.release()