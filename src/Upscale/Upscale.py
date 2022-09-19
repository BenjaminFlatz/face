from logging import captureWarnings
import cv2
from mss import mss
import os
import numpy as np
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
        
        parts = self.SplitImage(image)
        if image.shape[1] < self.maxWidth:

            return self.AddImages(parts[0], parts[1])
        else:
            leftPart = self.UpscaleOversizedImage(parts[0])
            rightPart = self.UpscaleOversizedImage(parts[1])
            return self.AddImages(parts[0], parts[1])

        
    def MagicMirror(self, image):
        
        parts = self.SplitImage(image)
        if image.shape[1] < self.maxWidth:
            upscaledLeft = self.sr.upsample(parts[0])
            upscaledRight = self.sr.upsample(parts[1])
            return self.AddImages(upscaledLeft, upscaledRight)
        else:
            leftPart = self.UpscaleOversizedImage(parts[0])
            rightPart = self.UpscaleOversizedImage(parts[1])
            return self.AddImages(leftPart, rightPart)

        
    def SplitImage(self, image):
        height, width, channels = image.shape
        half = width//2
        leftPart = image[:, :half] 
        rightPart = image[:, half:]
        cv2.imshow('upscaled', leftPart)
        cv2.imshow('upscaled', rightPart)

        return leftPart, rightPart

        
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

        try:
            if imagePath.endswith(self.imageFileExtensions):
                image = cv2.imread(imagePath)
                result = self.UpscaleOversizedImage(image)
                cv2.imwrite(outputPath, result)
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
            self.UpscaleVideo(capture, outputPath)
