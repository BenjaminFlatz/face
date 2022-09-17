
from .Upscale import Upscale

class ImageUpscaleService:
    def __init__(self, imagePath, modelPath, modelName, scaleFactor):
        self.upscale = Upscale()
        self.upscale.UpscaleImage(imagePath, modelPath, modelName, scaleFactor)

