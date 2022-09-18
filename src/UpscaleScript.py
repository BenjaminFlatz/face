from Upscale.ImageUpscaleService import ImageUpscaleService
from Upscale.ScreenUpscaleService import ScreenUpscaleService
from Upscale.VideoUpscaleService import VideoUpscaleService


if __name__ == '__main__':
    #image = ImageUpscaleService("images/test.jpg", "images/upscaled_lapsrn.jpg", "models/LapSRN_x4.pb", "lapsrn", 4)
    

    #image = ImageUpscaleService("images/test.jpg", "images/upscaled_test.jpg","models/EDSR_x4.pb", "edsr", 4)
    #image = ImageUpscaleService("images/upscaled_test_1.jpg","images/upscaled_test_2.jpg", "edsr", 4)
    #image = ImageUpscaleService("images/upscaled_test_2.jpg","mimages/upscaled_test_3.jpg", "edsr", 4)

    #screen = ScreenUpscaleService("models/ESPCN_x4.pb", "espcn", 4)
    
    #video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_espcn_x4.mp4", "models/ESPCN_x4.pb", "espcn", 4)
    #video = VideoUpscaleService("videos/test.mp4", "models/EDSR_x2.pb", "edsr", 2)
    #video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_edsr_x4.mp4","models/EDSR_x4.pb", "edsr", 4)

    video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_lapsrn_x8.mp4", "models/LapSRN_x8.pb", "lapsrn", 8)