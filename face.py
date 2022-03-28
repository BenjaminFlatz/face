import screeninfo
import argparse
from src.live_face_rec import LiveFaceRec


def get_window_size(monitorIndex):
    monitors = screeninfo.get_monitors()
    monitor = monitors[monitorIndex]

    if len(monitors) > 1:
        downscale = 1
    else:
        downscale = 2

    width = int(monitor.width/downscale)
    height = int(monitor.height/1)

    return width, height

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-r", "--record", help="record screen or camera", default='camera', type=str)
    parser.add_argument("-d", "--directory", help="directory for known face images", default='../learn', type=str)
    parser.add_argument("-s", "--size", help="window size width,height", default='800,800', type=str)
    parser.add_argument("-f", "--factor", help="down scale factor for image processing", default=1, type=int)
    parser.add_argument("-m", "--monitor", help="monitor index", default=0, type=int)
    args = parser.parse_args()

    width = int(args.size.split(',')[0])
    height = int(args.size.split(',')[1])
    #width, height = get_window_size(args.monitor)

    fr = LiveFaceRec(args.record, args.directory, width, height, args.factor)
    #fr.recordScreen()
    fr.searchFaceInImageDirectory("../images")