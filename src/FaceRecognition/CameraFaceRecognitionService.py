from .FaceRecognition import FaceRecognition

class CameraFaceRecognitionService:
    def __init__(self, learnDirectory, width, height, downscaleFactor):
        self.faceRecognition = FaceRecognition(learnDirectory, width, height, downscaleFactor)

    def Run(self):
        self.faceRecognition.RecordCamera()




