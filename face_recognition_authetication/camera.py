import cv2
import os

class VideoCamera(object):    
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def save_image(self, username):
        try:  
            os.mkdir("images\\"+username)
            goal_dir = os.path.join(os.getcwd(), "images\\"+username)
            path = os.path.join(os.path.abspath(goal_dir), 'myimage.jpg')
            retval, im = self.video.read()
            print("path = ", path)
            cv2.imwrite(path, im)
        except OSError:  
            print ("Creation of the directory %s failed" % username)
        else:  
            print ("Successfully created the directory %s " % username)
    
    def login(self):
        try:  
            #goal_dir = os.path.join(os.getcwd(), "login")
            #path = os.path.join(os.path.abspath(goal_dir), 'login.jpg')
            #print("path = ", path)
            retval, im = self.video.read()
            #cv2.imwrite(path, im)
            return im
        except OSError:  
            print ("Creation of the directory %s failed")
        else:  
            print ("Successfully created the directory %s ")
        
    