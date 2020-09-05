# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
#
#
# cred = credentials.Certificate("ai-translator-b30b8-firebase-adminsdk-6tcz4-8a6f19ae59.json")
# app = firebase_admin.initialize_app(cred)
# storage = app.storage()
#
# path_on_cloud = "images/"
# storage.child(path_on_cloud).download("test.jpg")

import pyrebase
import cv2
import pytesseract
import numpy as np
from firebase import firebase
import time
from googletrans import Translator
# Download tesseract and copy the path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

config = {
    "apiKey": "AIzaSyDQPmvl_1sCsrHXKct9nO0646knmKPDJSA",
    "authDomain": "ai-translator-b30b8.firebaseapp.com",
    "databaseURL": "https://ai-translator-b30b8.firebaseio.com",
    "projectId": "ai-translator-b30b8",
    "storageBucket": "ai-translator-b30b8.appspot.com",
    "messagingSenderId": "1031342738813",
    "appId": "1:1031342738813:web:fbc6f6d12e830c56af1014"
}
pathway2 = ""
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
translator = Translator()
# print(result)



while True:
    pathway = db.child("trans").get().val()
    if(pathway2 != pathway):
        app = storage.child("images/"+pathway).download("test1.jpg")
        image = "test1.jpg"

        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(img, lang="eng")
        translate = translator.translate(result, src="en", dest="zh-cn")
        print(result)
        print(pathway)

        data_to_upload = {
            "name": pathway,
            "text": result,
            "result": translate.text
        }
        db.child("pic").child(pathway).set(data_to_upload)
        pathway2 = pathway
        print(pathway2)
    time.sleep(5)



