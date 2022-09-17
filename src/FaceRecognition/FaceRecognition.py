import face_recognition
import cv2  # opencv-python
import numpy as np
import os
import numpy as np
from mss import mss
import shutil

class FaceRecognition:
    def __init__(self, learnDirectory, width, height, downscaleFactor):
        self.known_face_encodings = []
        self.known_face_names = []


        self.face_locations = []
        self.face_names = []
        self.face_encodings = []

        self.process = True
        self.downscaleFactor = downscaleFactor

        self.width = width
        self.height = height
        self.LearnFaces(learnDirectory)

        self.unknown = "unknown"
        self.no_face = "no face"
        self.fileExtensions = (".jpg", ".png", ".bmp")

    def LearnFaces(self, directory):

        print('Learning faces from ' + directory)
        for item in os.listdir(directory):
            self.known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(directory + os.path.sep + item))[0])
            self.known_face_names.append(item)

    def ProcessFrame(self, frame):
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
            return name
        self.process = not self.process
        return

    def RecordFrame(self, frame):
        
        small_frame = cv2.resize(frame, (0, 0), fx=1/self.downscaleFactor, fy=1/self.downscaleFactor)
        small_frame = small_frame[:, :, ::-1]
        
        self.ProcessFrame(small_frame)


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

    def RecordCamera(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Screen', self.RecordFrame(frame))
            if cv2.waitKey(1) == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()
            
    def RecordScreen(self):
        mon = {'top': 0, 'left': 0, 'width': self.width, 'height': self.height}
   
        with mss() as sct:
            while True:

                frame = cv2.cvtColor(np.array(sct.grab(mon)), cv2.COLOR_BGRA2BGR)
                cv2.imshow('Screen', self.RecordFrame(frame))

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()

    def SearchFaceInImageDirectory(self, directory: str):
        for filename in os.listdir(directory):
            if filename.endswith(self.fileExtensions):
                img = cv2.imread(directory + os.path.sep + filename)
                result = self.ProcessFrame(img)
                if result != None:
                    return result
                continue
            else:
                continue
        return



