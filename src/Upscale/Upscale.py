from logging import captureWarnings
from multiprocessing.connection import wait
import cv2
from mss import mss
import os
import numpy as np
import math
class Upscale:
    def __init__(self, modelPath, modelName, scaleFactor):
        self.modelPath = modelPath
        self.modelName = modelName
        self.scaleFactor = scaleFactor

        self.imageFileExtensions = (".jpg", ".jpeg", ".png", ".bmp")
        self.videoFileExtensions = (".mp4")
        self.maxWidth = 500
        self.maxHeight = 500

        cv2.cuda.printCudaDeviceInfo(0)
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        self.sr.readModel(self.modelPath)
        self.sr.setModel(self.modelName, self.scaleFactor)
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

    def UpscaleOversizedImage(self, image):
        
        height, width, channels = image.shape
        numberOfParts = math.ceil(width/self.maxWidth)
        newImage = (0,0,0)
        i = 0
        height, width, channels = image.shape  
        partWidth = width//numberOfParts
        cut = width-partWidth
        while i < numberOfParts:
            part = image[:, cut:]
            image = image[:, :cut]
            cut -= partWidth
            newImage += self.sr.upsample(part)
            cv2.imshow('part', part)
            cv2.waitKey(0)

            i += 1
        
        return newImage
      

        
    def SplitImage(self, image, numberOfParts):
        i = 0
        parts = []
        height, width, channels = image.shape  
        partWidth = width//numberOfParts
        rightPartWidth = partWidth
        while i < numberOfParts:
            leftPartWidth = width-rightPartWidth
            rightPartWidth += partWidth
            part = image[:, leftPartWidth:rightPartWidth]
            self.sr.upsample(part)
            parts.append(part)
        return parts

        
    def AddImages(self, leftPart, rightPart):
        return cv2.add(leftPart, rightPart)

    def UpscaleVideo(self, capture, outputPath):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(outputPath, fourcc, 29.97, (1920,1080))

        while capture.isOpened():
            ret, frame = capture.read()
            if ret == True: 
                upscaled = self.sr.upsample(frame)
                out.write(upscaled)
                cv2.imshow('upscaled', upscaled)
                #bicubic = cv2.resize(frame, 
                #    (upscaled.shape[1], upscaled.shape[0]),
                #    interpolation=cv2.INTER_CUBIC)

                #cv2.imshow("Original", frame)
                #cv2.imshow("Bicubic", bicubic)
                #cv2.imshow("Super Resolution", upscaled)
            else:
                break

            if cv2.waitKey(1) == ord("q"):
                break
        
        capture.release()   
        out.release()
        cv2.destroyAllWindows()

    def Image(self, imagePath: str, outputPath: str):


        if imagePath.endswith(self.imageFileExtensions):
            image = cv2.imread(imagePath)
            result = self.UpscaleOversizedImage(image)
            cv2.imwrite(outputPath, result)


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
            self.UpscaleVideo(capture, outputPath)
