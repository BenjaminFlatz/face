
from .Upscale import Upscale

class VideoUpscaleService:
    def __init__(self, modelPath, modelName, scaleFactor):
        self.upscale = Upscale(modelPath, modelName, scaleFactor)
        
    def UpscaleVideo(self, videoPath, outputPath, videoFormat):
        self.upscale.Video(videoPath, outputPath, videoFormat)

