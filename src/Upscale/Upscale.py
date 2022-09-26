from logging import captureWarnings
from multiprocessing.connection import wait
import cv2
from mss import mss
import os
import numpy as np
import math
import moviepy.editor as mp
class Upscale:
    def __init__(self, modelPath, modelName, scaleFactor):
        self.modelPath = modelPath
        self.modelName = modelName
        self.scaleFactor = scaleFactor

        self.imageFileExtensions = (".jpg", ".jpeg", ".png", ".bmp")
        self.videoFileExtensions = (".mp4", ".xvid", ".mkv")
        self.maxWidth = 500
        self.maxHeight = 500

        cv2.cuda.printCudaDeviceInfo(0)
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        self.sr.readModel(self.modelPath)
        self.sr.setModel(self.modelName, self.scaleFactor)
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

        
    def AddImages(self, leftImage, rightImage):
        ha,wa = leftImage.shape[:2]
        hb,wb = rightImage.shape[:2]
        max_height = np.max([ha, hb])
        total_width = wa+wb
        new_img = np.zeros(shape=(max_height, total_width, 3))
        new_img[:ha,:wa]=leftImage
        new_img[:hb,wa:wa+wb]=rightImage
        return new_img
        return cv2.add(leftPart, rightPart)

    def UpscaleVideo(self, videoPath, outputPath):
        capture = cv2.VideoCapture(videoPath)
        fps = capture.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(outputPath, fourcc, fps, (1080, 1920))
        
        while capture.isOpened():
            grabbed, frame = capture.read()
            if grabbed:
                upscaled = self.sr.upsample((frame).astype(np.uint8))
                out.write(upscaled)
                cv2.imshow('upscaled', frame)
            else:
                break

            if cv2.waitKey(1) == ord("q"):
                break
    

        capture.release()   
        out.release()
        cv2.destroyAllWindows()
        return 


    def Image(self, imagePath: str, outputPath: str):

        if imagePath.endswith(self.imageFileExtensions):
            image = cv2.imread(imagePath)
            result = self.sr.upsample((image).astype(np.uint8))
            cv2.imwrite(outputPath, result)


    def Screen(self, x, y, width, height):
        mon = {'top': x, 'left': y, 'width': width, 'height': height}
   
        with mss() as sct:
            while True:

                frame = cv2.cvtColor(np.array(sct.grab(mon)), cv2.COLOR_BGRA2BGR)
                upscaled = self.sr.upsample((frame).astype(np.uint8))
                cv2.imshow('Screen', upscaled)

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()
    
    
    def Video(self, videoPath: str, outputPath: str):
        if videoPath.endswith(self.videoFileExtensions):
            self.UpscaleVideo(videoPath, outputPath)
            clip = mp.VideoFileClip(videoPath)
            upscaledClip = mp.VideoFileClip(outputPath)
            upscaledClip = upscaledClip.set_audio(clip.audio)
            upscaledClip.write_videofile(outputPath)
