# Face Id Authentication

## Description
This is a flask project to register users with their face as an identifier and then allowing them to login into the system back with the same.

### Softwares you need

- Python 3.x
- opencv-python
- opencv-contrib-python 
- flask
 
 For installation you can use pip installer For ex
 > pip install flask

### File Description

-  **main.py** :- Main flask application file. We will start our app by running this file only
-  **camera.py** :- contains all camera related operation . for ex :- saving image, creating frame
-  **train.py** :- Contains LBPH image training model. Also has functions for preparing training data, performing model training and making                    predictions
-  **index.html** :- Primary landing page for our application. Contains two links to register and to login.
-  **login.html** :- Allows user to login after scanning their face
-  **register.html** :- Allows user to register themselves.

### Capturing image

As per code when user clicks on register link capture function gets called inside main.py. This function simply captures the image of the user and saves it inside **images** folder inside a sub directory having same name as the username.

```
def capture():
    username = request.json
    usernames.append(username)
    print(" username  = ", type(username))
    cam.save_image(username)
    return Response("success", mimetype='text/plain')
```
After registeration user gets a message that he/she has been registered

### Logging in

Now when we go back to the home page and click on **Login** link then we will get redirected to another page which is **login.html**. This page again opens up a camera with a button called as **Login** beside it. Once you click on login camera again captures the image and sends it back to the backend to login function. This function starts training our model with all the images present in images directory and then makes a prediction over the newly captured image. This logs in the user

```

@app.route('/login' ,methods = ['POST', 'GET'])
def login():
    test_img1 = cam.login()
    tn = train_data()
    predicted_img1, label = tn.predict(test_img1) 
    print("Prediction complete ", predicted_img1)
    return Response(usernames[label], mimetype='text/plain')
```
 
 
 ### Training model used
 
 We have used here LBPHFaceRecognizer model to make predictions. Faces in training images are classified using OpenCV with **lbpcascade_frontalface.xml** for face detection.
 
 > self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
 
 ```
 def detect_face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
        if (len(faces) == 0):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y+w, x:x+h], faces[0]
 ```
 
 With detect_face function we are preparing training data. In the below function images of all registered users are taken and converted into matrix by detect_face function. Each matrix is mapped to its label which in our case is the username or sub directory name. This list of matrices and labels is returned as X and Y from prepare_training_data function
 
 ```
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
```

After training data is prerared we can feed it to the model

```
def train(self, faces, labels):
        self.face_recognizer.train(faces, np.array(labels))
```

After training its pretty easy to make predictions. New image is also detected with a face and that face matrix is then used to make prediction. Predicted label or username is returned back to the calling login function and then its dispalayed on the screen

```
def predict(self, test_img):
        img = test_img.copy()
        face, rect = self.detect_face(img)
        label = self.face_recognizer.predict(face)
        label_text = self.usernames[label[0]]
        return img, label[0]
```


# That! all. Have fun trying this out
 
