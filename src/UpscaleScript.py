from Upscale.ImageUpscaleService import ImageUpscaleService
from Upscale.ScreenUpscaleService import ScreenUpscaleService
from Upscale.VideoUpscaleService import VideoUpscaleService


if __name__ == '__main__':
    #image = ImageUpscaleService("images/test.jpg", "images/upscaled.jpg","models/EDSR_x4.pb", "edsr", 4)
    image = ImageUpscaleService("images/test.jpg", "images/upscaled.jpg", "models/LapSRN_x2.pb", "lapsrn", 2)
    
    #screen = ScreenUpscaleService("models/ESPCN_x4.pb", "espcn", 4)
    #video = VideoUpscaleService("videos/test.mp4", "models/ESPCN_x2.pb", "espcn", 2)
    #video = VideoUpscaleService("videos/test.mp4", "models/EDSR_x2.pb", "edsr", 2)
    video = VideoUpscaleService("videos/test.mp4", "models/LapSRN_x2.pb", "lapsrn", 2)