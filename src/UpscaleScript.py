from Upscale.ImageUpscaleService import ImageUpscaleService
from Upscale.ScreenUpscaleService import ScreenUpscaleService
from Upscale.VideoUpscaleService import VideoUpscaleService


if __name__ == '__main__':
    #image = ImageUpscaleService("images/test.jpg", "images/upscaled_lapsrn.jpg", "models/LapSRN_x4.pb", "lapsrn", 4)
    #image = ImageUpscaleService("images/oversize.jpeg", "images/upscaled_oversize_lapsrn.jpeg", "models/LapSRN_x4.pb", "lapsrn", 4)


    #image = ImageUpscaleService("images/forest.jpeg", "images/forest_edsr4.jpeg","models/EDSR_x4.pb", "edsr", 4)
    #image = ImageUpscaleService("images/upscaled_test_1.jpg","images/upscaled_test_2.jpg", "edsr", 4)
    #image = ImageUpscaleService("images/upscaled_test_2.jpg","mimages/upscaled_test_3.jpg", "edsr", 4)

    #screen = ScreenUpscaleService("models/ESPCN_x4.pb", "espcn", 4)
    
    video = VideoUpscaleService("videos/test_hd.mkv", "videos/upscaled_espcn_x2.mkv", "models/ESPCN_x2.pb", "espcn", 2)
    #video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_espcn_x2.mp4", "models/ESPCN_x2.pb", "espcn", 2)    
    
    #video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_edsr_x4.mp4","models/EDSR_x4.pb", "edsr", 4)
    #video = VideoUpscaleService("videos/test.mp4", "videos/upscaled_lapsrn_x4.mp4", "models/LapSRN_x4.pb", "lapsrn", 4)