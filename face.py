
import argparse
from src.live_face_rec import LiveFaceRec


if __name__ == '__main__':


    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-r", "--record", help="record screen or camera", default='camera', type=str)
    parser.add_argument("-d", "--directory", help="directory for known face images", default='faces', type=str)
    parser.add_argument("-m", "--monitor", help="monitor index", default=0, type=int)
    args = parser.parse_args()


    fr = LiveFaceRec(args.record, args.directory, args.monitor)
    fr.run()