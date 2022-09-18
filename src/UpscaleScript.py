from Upscale.ImageUpscaleService import ImageUpscaleService
from Upscale.ScreenUpscaleService import ScreenUpscaleService
from Upscale.VideoUpscaleService import VideoUpscaleService


if __name__ == '__main__':
    #image = ImageUpscaleService("images/test.jpg", "images/upscaled.jpg","models/EDSR_x4.pb", "edsr", 4)
    #screen = ScreenUpscaleService("models/espcn_x4.pb", "espcn", 4)
    #video = VideoUpscaleService("videos/test.mp4", "models/espcn_x4.pb", "espcn", 4)
    video = VideoUpscaleService("videos/test.mp4", "models/EDSR_x2.pb", "edsr", 2)