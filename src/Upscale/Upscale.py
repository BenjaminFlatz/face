from cv2 import dnn_superres
import cv2

class Upscale:
    def __init__(self):
        self.fileExtensions = (".jpg", ".png", ".bmp")
        self.sr = dnn_superres.DnnSuperResImpl_create()
      
    def UpscaleImage(self, imagePath, modelPath, modelName, scaleFactor):

        if imagePath.endswith(self.fileExtensions):
            image = cv2.imread(imagePath)
            self.sr.readModel(modelPath)
            self.sr.setModel(modelName, scaleFactor)
            result = self.sr.upsample(image)
            cv2.imwrite("./upscaled.png", result)

    