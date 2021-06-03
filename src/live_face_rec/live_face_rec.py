import time
import face_recognition
import cv2  # opencv-python
import numpy as np
import os
import numpy as np
from mss import mss
import screeninfo


class LiveFaceRec:
    def __init__(self, record, directory, monitor):
        self.known_face_encodings = []
        self.known_face_names = []


        self.face_locations = []
        self.face_names = []
        self.face_encodings = []

        self.process = True
        
        self.record = record

        self.width, self.height = self.get_window_size(monitor)
        self.learn_faces(directory)


    def get_window_size(self, monitorIndex):

        monitors = screeninfo.get_monitors()
        monitor = monitors[monitorIndex]
        if len(monitors) > 1:
            monitorDownscale = 1
        
        else:
            monitorDownscale = 2
        
        width = int(monitor.width/monitorDownscale)
        height = int(monitor.height/monitorDownscale)

        return width, height

    def learn_faces(self, directory):

        print('Learning faces from ' + directory)

        for item in os.listdir(directory):
            self.known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(directory + os.path.sep + item))[0])
            self.known_face_names.append(item.split(".")[0])


    def process_frame(self, frame):

        if self.process:

            self.face_locations = face_recognition.face_locations(frame)
            self.face_encodings = face_recognition.face_encodings(frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
             
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

             
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

        self.process = not self.process


    def get_frame(self, frame):
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame = small_frame[:, :, ::-1]
        
        self.process_frame(small_frame)


        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top),(right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35),(right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),font, 1.0, (255, 255, 255), 1)
        
        
        return frame     

    def rec_camera(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Screen', self.get_frame(frame))
            if cv2.waitKey(1) == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()
            
    def rec_screen(self):
        mon = {'top': 0, 'left': 0, 'width': self.width, 'height': self.height}
   
        with mss() as sct:
            while True:

                frame = cv2.cvtColor(np.array(sct.grab(mon)), cv2.COLOR_BGRA2BGR)
                cv2.imshow('Screen', self.get_frame(frame))

                if cv2.waitKey(1) == ord("q"):
                    break

            cv2.destroyAllWindows()

    def run(self):
        
        if self.record == 'camera':
            self.rec_camera()
        elif self.record == 'screen':
            self.rec_screen()
        else:
            print('Choose a correct mode!')

           




