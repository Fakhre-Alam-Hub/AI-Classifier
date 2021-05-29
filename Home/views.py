from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import os
import numpy as np
import dlib
from keras.models import load_model

# Model saved with Keras model.save()
MODEL_PATH = 'models/person_classification'

# Load your trained model
model = load_model(MODEL_PATH)

persons_label = [
                'AAMIR KHAN', 'ALBERT EINSTEIN', 'AMITABH BACHCHAN', 'APJ ABDUL KALAM',
                'BARACK OBAMA', 'ELON MUSK', 'JEFF BEZOS', 'RATAN TATA', 'SACHIN TENDULKAR',
                'SUNDAR PICHAI'
                ]

# Dlib face detector object
detector = dlib.get_frontal_face_detector()

# Create your views here.
def index(request):
    return render(request, 'Home/index.html')

def predictImage(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        fileObj = request.FILES['filePath']
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)

        # Making Prediction on image
        frame =cv2.imread("media/"+str(fileObj))
        
        faces = detector(frame)  # detects multiple face
        face = faces[0]
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()

        # Crop face from image
        imgCrop = frame[y1:y2, x1:x2]
        width, height = (224,224)
        imgCrop = cv2.resize(imgCrop, (width, height))

        # Normalize
        imgCrop = np.array(imgCrop)
        imgCrop_scaled = imgCrop/255

        # Make prediction
        pred = model.predict(np.expand_dims(imgCrop_scaled,axis=0))
        name = persons_label[pred.argmax()]

        # name = "default"
        return render(request, 'Home/index.html', {"filePathName":filePathName, "name":name})

    else:
        return render(request, 'Home/index.html')


def about(request):
    return render(request, 'Home/about.html')


def contact(request):
    return render(request, 'Home/contact.html')