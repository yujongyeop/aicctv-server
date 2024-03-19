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