from .FaceRecognition import FaceRecognition

class ScreenFaceRecognitionService:
    def __init__(self, learnDirectory, width, height, downscaleFactor):
        self.faceRecognition = FaceRecognition(learnDirectory, width, height, downscaleFactor)

    def Run(self):
        self.faceRecognition.RecordScreen() 






