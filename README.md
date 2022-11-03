# Face

This project is split up into several parts.
All of them are implementations of some machine learning program.


## 1. Face recognition
Project to recognize known faces on camera, sceen or images. It uses the face_recognition package and only runs on the CPU.

### optional arguments
```
  -h     --help      show this help message and exit
  -r     --record    record screen or camera (default: camera)
  -d     --directory directory for known face images (default: faces)
  -s     --size      window size width,height (default: 800,800)
  -f     --factor    down scale factor for image processing (default: 4)
  -m     --monitor   monitor index (default: 0)
```

## 2. Upscale
The focus of this project is to upsample images and videos. It uses the cv2 package and can use the GPU.


