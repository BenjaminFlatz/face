
from .Upscale import Upscale

class ScreenUpscaleService:
    def __init__(self, modelPath, modelName, scaleFactor):
        self.upscale = Upscale(modelPath, modelName, scaleFactor)

    def Run(self, x=0, y=0, width=500, height=500):
        self.upscale.Screen(x, y, width, height)
