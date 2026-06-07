import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import requests
import time

# 🔥 CHANGE THIS
URL = "http://127.0.0.1:8000/sign-message/1/"

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

labels = ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P",
          "Q","R","S","T","U","V","W","X","Y","SPACE"]

last_sent = ""
last_time = 0
delay = 2  # seconds

word = ""

while True:
    success, img = cap.read()
    imgOutput = img.copy()

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        detected_text = labels[index]

        # 🧠 WORD BUILDING
        if detected_text != "SPACE":
            word += detected_text

        # 🧠 SEND WORD WHEN SPACE
        if detected_text == "SPACE" and word != "":
            if time.time() - last_time > delay:
                try:
                    requests.post(URL, data={"msg": word})
                    print("Sent:", word)
                    word = ""
                    last_time = time.time()
                except:
                    print("Error sending")

        # 🎯 UI DRAWING
        cv2.rectangle(imgOutput, (x-offset, y-offset-70),
                      (x-offset+400, y-offset-10),
                      (0,255,0), cv2.FILLED)

        cv2.putText(imgOutput, detected_text, (x, y-30),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 2)

        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x+w+offset, y+h+offset),
                      (0,255,0), 4)

        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)