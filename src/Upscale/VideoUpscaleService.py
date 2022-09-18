
from .Upscale import Upscale

class VideoUpscaleService:
    def __init__(self, videoPath, modelPath, modelName, scaleFactor):
        self.upscale = Upscale(modelPath, modelName, scaleFactor)
        self.upscale.Video(videoPath, outputPath=".")

