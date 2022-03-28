import face_recognition
import cv2  # opencv-python
import numpy as np
import os
import numpy as np
from mss import mss
import shutil

class LiveFaceRec:
    def __init__(self, record, directory, width, height, downscaleFactor):
        self.known_face_encodings = []
        self.known_face_names = []


        self.face_locations = []
        self.face_names = []
        self.face_encodings = []

        self.process = True
        self.downscaleFactor = downscaleFactor
        self.record = record

        self.width = width
        self.height = height
        self.learnFaces(directory)

        self.unknown = "unknown"
        self.no_face = "no face"

    def learnFaces(self, directory):

        print('Learning faces from ' + directory)

        for item in os.listdir(directory):
            self.known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(directory + os.path.sep + item))[0])
            self.known_face_names.append(item.split(".")[0])

    def processFrame(self, frame):
        name = self.no_face
        if self.process:

            self.face_locations = face_recognition.face_locations(frame)
            self.face_encodings = face_recognition.face_encodings(frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
             
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = self.unknown

             
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

        self.process = not self.process
        return name

    def recordFrame(self, frame):
        
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.downscaleFactor, fy=1/self.downscaleFactor)
        small_frame = small_frame[:, :, ::-1]
        
        self.processFrame(small_frame)


        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= self.downscaleFactor
            right *= self.downscaleFactor
            bottom *= self.downscaleFactor
            left *= self.downscaleFactor
            cv2.rectangle(frame, (left, top),(right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35),(right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),font, 1.0, (255, 255, 255), 1)
        
        
        return frame     

    def recordCamera(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Screen', self.recordFrame(frame))
            if cv2.waitKey(1) == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()
            
    def recordScreen(self):
        mon = {'top': 0, 'left': 0, 'width': self.width, 'height': self.height}
   
        with mss() as sct:
            while True:

                frame = cv2.cvtColor(np.array(sct.grab(mon)), cv2.COLOR_BGRA2BGR)
                cv2.imshow('Screen', self.recordFrame(frame))

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()

    def searchFaceInImageDirectory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                img = cv2.imread(directory + os.path.sep + filename)
                result = self.processFrame(img)
                if result != self.no_face:
                    shutil.copy2(directory + os.path.sep + filename, directory + os.path.sep + "out" + os.path.sep  + filename) # complete target filename given
                    print(result + "," + filename)
                continue
            else:
                continue

    def scanImagesForFaces(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                img = cv2.imread(directory + os.path.sep + filename)
                result = self.processFrame(img)
                if result != self.no_face:
                    shutil.copy2('/src/dir/file.ext', '/dst/dir/newname.ext') # complete target filename given
                    print(result + "," + filename)
                continue
            else:
                continue

    

    def run(self):
        
        if self.record == 'camera':
            self.recordCamera()
        elif self.record == 'screen':
            self.recordScreen() 
        elif self.record == 'directory':
            self.searchFaceInImageDirectory("images")
        else:
            print('Choose a correct mode!')





