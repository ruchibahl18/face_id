import cv2
import os
import numpy as np

class TrainData:
    def __init__(self, usernames):
        self.usernames = usernames
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def detect_face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
        if (len(faces) == 0):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y+w, x:x+h], faces[0]
    
    def prepare_training_data(self):
        data_folder_path = os.path.join(os.getcwd(), "images")
        dirs = os.listdir(data_folder_path)
        faces = []
        labels = []
        for dir_name in dirs:
            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)
            for image_name in subject_images_names: 
                image_path = subject_dir_path + "/" + image_name
                image = cv2.imread(image_path)
                cv2.waitKey(100)
                face, rect = self.detect_face(image)
                print("faces ", face)
                if face is not None:
                    print(" face found")
                    faces.append(face)
                    labels.append(self.usernames.index(dir_name))
        return faces, labels
    
    def train(self, faces, labels):
        self.face_recognizer.train(faces, np.array(labels))
    
    def draw_rectangle(self, img, rect):
       (x, y, w, h) = rect
       cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
    def draw_text(self, img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        
    def predict(self, test_img):
        img = test_img.copy()
        face, rect = self.detect_face(img)
        label = self.face_recognizer.predict(face)
        label_text = self.usernames[label[0]]
        self.draw_rectangle(img, rect)
        self.draw_text(img, label_text, rect[0], rect[1]-5)
        return img, label[0]
