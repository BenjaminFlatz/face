from array import array
from .FaceRecognition import FaceRecognition

class .ImageFaceRecognitionService:
    def __init__(self, learnDirectory, width, height, downscaleFactor):
        self.faceRecognition = FaceRecognition(learnDirectory, width, height, downscaleFactor)

    def Run(self):
        names=[]
        names.append(self.faceRecognition.SearchFaceInImageDirectory("images"))
        print(names)






