

import argparse
from lib import FaceRec



if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-r", "--rec", help="record screen or camera", default='cam', type=str)
    parser.add_argument("-s", "--scaleFactor", help="Scale factor for faster image processing (factor < 1)", default=0.25, type=float)
    parser.add_argument("-d", "--directory", help="directory for known face images", default='faces', type=str)
    parser.add_argument("-m", "--monitor", help="monitor width,height", default='500,500', type=str)

    args = parser.parse_args()
    width = int(args.monitor.split(',')[0])
    height = int(args.monitor.split(',')[1])

    fr = FaceRec(args.rec, args.scaleFactor, args.directory, width, height)
    fr.run()