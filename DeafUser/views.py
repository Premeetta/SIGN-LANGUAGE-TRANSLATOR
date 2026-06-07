from django.shortcuts import render,redirect
from DeafUser.models import *
from Admin.models import*
from Guest.models import*
from User.models import*
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

def HomePage(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_deafuser.objects.get(id=request.session['duid'])
    return render(request,'DeafUser/HomePage.html',{'data':data})

def MyProfile(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_deafuser.objects.get(id=request.session['duid'])
    return render(request,'DeafUser/MyProfile.html',{'data':data})

def EditProfile(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_deafuser.objects.get(id=request.session['duid'])
    if request.method=="POST":
        data.deafuser_name=request.POST.get('txt_name')
        data.deafuser_email=request.POST.get('mail')
        data.deafuser_address=request.POST.get('txt_address')
        data.save()
        return render(request,'DeafUser/EditProfile.html',{'msg':"profile Updated"})
    else:
        return render(request,'DeafUser/EditProfile.html',{'data':data})

def ChangePassword(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_deafuser.objects.get(id=request.session['duid'])
    if request.method == "POST":
        Old_Password = request.POST.get('old_pass')
        New_Password = request.POST.get('new_pass')
        Re_type = request.POST.get('re_pass')
        password=data.deafuser_password
        if Old_Password == password:
            if New_Password == Re_type:
                data.user_password=Re_type
                data.save()
                return render(request,'DeafUser/ChangePassword.html',{'msg':"Password Updated"})

            else:
                return render(request,'DeafUser/ChangePassword.html',{'msg':"Password Mismatched"})

        else:
            return render(request,'DeafUser/ChangePassword.html',{'msg':"Enter Correct Password"})

    return render(request,'DeafUser/ChangePassword.html')
# Create your views here.


def UserList(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_user.objects.all()
    return render(request,'DeafUser/UserList.html',{'abcd':data})

def sendrequest(request,uid):
    user=tbl_user.objects.get(id=uid)
    deafuser=tbl_deafuser.objects.get(id=request.session['duid'])
    tbl_request.objects.create(user_id=user,deafuser_id=deafuser)
    return render(request,'DeafUser/UserList.html',{'msg':"Request Send"})

def myrequest(request):
    reqdata=tbl_request.objects.filter(deafuser_id=request.session['duid'])
    return render(request,'DeafUser/MyRequest.html',{'reqdata':reqdata})


def Complaint(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    userid=tbl_deafuser.objects.get(id=request.session['duid'])
    complaintdata=tbl_complaint.objects.filter(deafuser_id=request.session['duid'])
    if request.method == "POST":
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,deafuser_id=userid)
        return render(request,'DeafUser/Complaint.html',{'msg':"Inserted"})
    else:   
        return render(request,'DeafUser/Complaint.html',{'complaintdata':complaintdata})

def logout(request):
    if 'duid' not in request.session:
        return redirect('Guest:Login')
    del request.session['duid']
    return redirect("Guest:Index")

def DeafChat(request, uid):
    if 'duid' not in request.session:
        return redirect('Guest:Login')

    deaf = tbl_deafuser.objects.get(id=request.session['duid'])
    user = tbl_user.objects.get(id=uid)

    if request.method == "POST":
        msg = request.POST.get('msg')
        tbl_chat.objects.create(
            from_deaf=deaf,
            to_user=user,
            message=msg
        )
        return JsonResponse({'status': 'sent'})

    return render(request, 'DeafUser/Chat.html', {'user': user,'duid': request.session['duid']})


def get_messages_deaf(request, uid):
    deaf = tbl_deafuser.objects.get(id=request.session['duid'])
    user = tbl_user.objects.get(id=uid)

    chats = tbl_chat.objects.filter(
        Q(from_user=user, to_deaf=deaf) |
        Q(from_deaf=deaf, to_user=user)
    ).order_by('date')

    data = []
    for c in chats:
        data.append({
            'msg': c.message,
            'type': 'sent' if c.from_deaf else 'received'
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def sign_message(request, uid):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            msg = data.get("msg", "").strip()
            deaf_id = data.get("deaf_id")

            # ❌ STOP empty messages
            if not msg:
                return JsonResponse({"status": "empty"}, status=400)

            deaf = tbl_deafuser.objects.get(id=deaf_id)
            user = tbl_user.objects.get(id=uid)

            tbl_chat.objects.create(
                from_deaf=deaf,
                to_user=user,
                message=msg
            )

            return JsonResponse({"status": "sent"})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"status": "error"}, status=500)
import base64
import math
import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from DeafUser.models import *
from User.models import *

detector = None
classifier = None


def load_sign_detector():
    global detector, classifier

    if detector is not None and classifier is not None:
        return detector, classifier

    from cvzone.HandTrackingModule import HandDetector
    from cvzone.ClassificationModule import Classifier

    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
    return detector, classifier

offset = 20
imgSize = 300

labels = ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P",
          "Q","R","S","T","U","V","W","X","Y","SPACE"]

word_buffer = ""
last_time = 0
delay = 2

frame_buffer = []
buffer_size = 8   # total frames to check
threshold = 5 
final_text=""
@csrf_exempt
def detect_sign(request, uid):
    final_text =""
    global word_buffer, last_time

    if request.method == "POST":
        try:
            import cv2
            import numpy as np
            detector, classifier = load_sign_detector()
        except ImportError:
            return JsonResponse({
                "status": "unavailable",
                "message": "Sign detection is not available on this deployment."
            }, status=503)

        body = json.loads(request.body)

        image_data = body.get("image")
        deaf_id = body.get("deaf_id")

        # 🔥 Decode base64 → OpenCV image
        format, imgstr = image_data.split(';base64,')
        img_bytes = base64.b64decode(imgstr)
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        imgOutput = img.copy()

        hands, img = detector.findHands(img)

        detected_text = ""

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

            # 🔥 SAFE CROP (IMPORTANT FIX)
            y1 = max(0, y-offset)
            y2 = min(img.shape[0], y + h + offset)
            x1 = max(0, x-offset)
            x2 = min(img.shape[1], x + w + offset)

            imgCrop = img[y1:y2, x1:x2]

            if imgCrop.size != 0:
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

                # prediction, index = classifier.getPrediction(imgWhite, draw=False)
                # detected_text = labels[index]

                # # 🧠 WORD BUILDING (same logic as your script)
                # if detected_text != "SPACE":
                #     word_buffer += detected_text

                # if detected_text == "SPACE" and word_buffer != "":
                #     if time.time() - last_time > delay:
                #         deaf = tbl_deafuser.objects.get(id=deaf_id)
                #         user = tbl_user.objects.get(id=uid)

                #         tbl_chat.objects.create(
                #             from_deaf=deaf,
                #             to_user=user,
                #             message=word_buffer
                #         )

                #         print("Sent:", word_buffer)

                #         word_buffer = ""
                #         last_time = time.time()
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                detected_text = labels[index]

                # 🧠 FRAME SMOOTHING
                frame_buffer.append(detected_text)

                if len(frame_buffer) > buffer_size:
                    frame_buffer.pop(0)

                final_text = ""

                # 🔥 CHECK STABILITY
                if len(frame_buffer) == buffer_size:
                    counts = {}

                    for item in frame_buffer:
                        counts[item] = counts.get(item, 0) + 1

                    most_common = max(counts, key=counts.get)

                    if counts[most_common] >= threshold:
                        final_text = most_common

                        # 🔥 CLEAR BUFFER AFTER CONFIRM
                        frame_buffer.clear()

                # 🧠 WORD BUILDING (ONLY STABLE TEXT)
                if final_text:
                    if final_text != "SPACE":
                        word_buffer += final_text

                    if final_text == "SPACE" and word_buffer != "":
                        if time.time() - last_time > delay:
                            deaf = tbl_deafuser.objects.get(id=deaf_id)
                            user = tbl_user.objects.get(id=uid)

                            tbl_chat.objects.create(
                                from_deaf=deaf,
                                to_user=user,
                                message=word_buffer
                            )

                            print("Sent:", word_buffer)

                            word_buffer = ""
                            last_time = time.time()
        return JsonResponse({
            "text": final_text,
            "current_word": word_buffer
        })
