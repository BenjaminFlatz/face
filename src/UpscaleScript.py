from Upscale.ImageUpscaleService import ImageUpscaleService


if __name__ == '__main__':
    #fr = ImageUpscaleService("images/test.jpg","models/EDSR_x4.pb", "edsr", 4)
    fr = ImageUpscaleService("images/test.jpg","models/espcn_x2.pb", "espcn", 2)