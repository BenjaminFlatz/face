
from .Upscale import Upscale

class ImageUpscaleService:
    def __init__(self, imagePath, outputPath, modelPath, modelName, scaleFactor):
        self.upscale = Upscale( modelPath, modelName, scaleFactor)
        self.upscale.Image(imagePath, outputPath)

