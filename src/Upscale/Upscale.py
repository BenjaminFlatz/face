from logging import captureWarnings
from cv2 import dnn_superres
import cv2
from mss import mss
import os
import numpy as np
class Upscale:
    def __init__(self, modelPath, modelName, scaleFactor):
        self.modelPath = modelPath
        self.modelName = modelName
        self.scaleFactor = scaleFactor

        self.imageFileExtensions = (".jpg", ".png", ".bmp")
        self.videoFileExtensions = (".mp4")

        self.sr = dnn_superres.DnnSuperResImpl_create()
        self.sr.readModel(self.modelPath)
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setPreferableTarget(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setModel(self.modelName, self.scaleFactor)


    def UpscaleVideo(self, capture):
        while capture.isOpened():
            ret, frame = capture.read()
            if ret == True: 
                upscaled = self.sr.upsample(frame)
                bicubic = cv2.resize(frame,
                    (upscaled.shape[1], upscaled.shape[0]),
                    interpolation=cv2.INTER_CUBIC)

                #cv2.imshow("Original", frame)
                cv2.imshow("Bicubic", bicubic)
                cv2.imshow("Super Resolution", upscaled)
            else:
                break

            if cv2.waitKey(1) == ord("q"):
                break
          


    def Image(self, imagePath: str, outputPath: str):

        try:
            if imagePath.endswith(self.imageFileExtensions):
                image = cv2.imread(imagePath)
           
                result = self.sr.upsample(image)
                cv2.imwrite(outputPath + os.path.sep + "upscaled.png", result)
        except Exception as e:
            print(e)

    def Screen(self, x, y, width, height):
        mon = {'top': x, 'left': y, 'width': width, 'height': height}
   
        with mss() as sct:
            while True:

                frame = cv2.cvtColor(np.array(sct.grab(mon)), cv2.COLOR_BGRA2BGR)
                upscaled = self.sr.upsample(frame)
                cv2.imshow('Screen', upscaled)

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()
    
    
    def Video(self, videoPath: str, outputPath: str):
        
        if videoPath.endswith(self.videoFileExtensions):
            capture = cv2.VideoCapture(videoPath)
            self.sr.readModel(self.modelPath)
            self.sr.setModel(self.modelName, self.scaleFactor)
            self.UpscaleVideo(capture)


