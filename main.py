from logging import captureWarnings
from cv2 import dnn_superres
import cv2
from mss import mss
import os
import numpy as np


if __name__ == "__main__":

    print("cv2 version",cv2.__version__)
    image = cv2.imread("images/test.jpg")
    cv2.imshow("image",image)
    cv2.waitKey(0)
    # Create an SR object
    modelPath = "models/LapSRN_x8.pb"


    cv2.cuda.printCudaDeviceInfo(0)
    cv2.cuda.setDevice(0)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(modelPath)
    sr.setModel("lapsrn", 8)
    sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    sr.setPreferableTarget(cv2.dnn.DNN_BACKEND_CUDA)
    # Read the desired model

    # Set the desired model and scale to get correct pre- and post-processing

    # Upscale the image
    result = sr.upsample(image)
    cv2.imshow("Output",result)