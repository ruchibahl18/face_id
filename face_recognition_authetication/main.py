#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response,request
from camera import VideoCamera
from train import TrainData
import os
import cv2

app = Flask(__name__)
usernames= [""]


#login_cam = VideoCamera()

def train_data():
    data_folder_path = os.path.join(os.getcwd(), "images")
    dirs = os.listdir(data_folder_path)
    for dir_name in dirs:
        usernames.append(dir_name)
    print("usernames ", usernames)
    tn = TrainData(usernames)
    faces , labels = tn.prepare_training_data()
    tn.train(faces, labels)
    return tn

@app.route('/video_feed')
def video_feed():
    global cam
    cam = VideoCamera()
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
#@app.route('/video_feed_login')
#def video_feed_login():  
#    return Response(gen(login_cam),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/capture' ,methods = ['POST', 'GET'])
def capture():
    username = request.json
    usernames.append(username)
    print(" username  = ", type(username))
    cam.save_image(username)
    return Response("success", mimetype='text/plain')

@app.route('/login' ,methods = ['POST', 'GET'])
def login():
    test_img1 = cam.login()
    tn = train_data()
    predicted_img1, label = tn.predict(test_img1)
   
    print("Prediction complete ", predicted_img1)
    #cv2.imshow(usernames[label], predicted_img1)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return Response(usernames[label], mimetype='text/plain')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)