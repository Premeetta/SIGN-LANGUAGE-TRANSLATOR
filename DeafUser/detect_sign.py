import base64
import numpy as np
import cv2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# load model once globally
from cvzone.ClassificationModule import Classifier
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

labels = ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P",
          "Q","R","S","T","U","V","W","X","Y","SPACE"]


@csrf_exempt
def detect_sign(request, uid):
    if request.method == "POST":
        body = json.loads(request.body)

        image_data = body.get("image")
        deaf_id = body.get("deaf_id")

        # 🔥 Decode base64 image
        format, imgstr = image_data.split(';base64,')
        img_bytes = base64.b64decode(imgstr)
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # 🔥 Resize for model
        img = cv2.resize(img, (300, 300))

        prediction, index = classifier.getPrediction(img, draw=False)
        detected_text = labels[index]

        # 🔥 Save message if SPACE
        if detected_text == "SPACE":
            # send accumulated word (optional logic)
            pass

        return JsonResponse({
            "text": detected_text
        })