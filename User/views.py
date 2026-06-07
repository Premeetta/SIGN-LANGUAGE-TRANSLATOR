from django.shortcuts import render,redirect
from Guest.models import *
from User.models import *

import cv2
import mediapipe as mp
import copy
import itertools
import numpy as np
import pandas as pd
import string
from tensorflow import keras
from django.shortcuts import render

from textblob import TextBlob

# Create your views here.
def HomePage(request):
    data=tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/HomePage.html',{'data':data})

def MyProfile(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/MyProfile.html',{'data':data})

def EditProfile(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        data.user_name=request.POST.get('txt_name')
        data.user_email=request.POST.get('mail')
        data.user_contact=request.POST.get('txt_contact')
        data.user_address=request.POST.get('txt_address')
        data.save()
        return render(request,'User/EditProfile.html',{'msg':"profile Updated"})
    else:
        return render(request,'User/EditProfile.html',{'data':data})

def ChangePassword(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    data=tbl_user.objects.get(id=request.session['uid'])
    if request.method == "POST":
        Old_Password = request.POST.get('old_pass')
        New_Password = request.POST.get('new_pass')
        Re_type = request.POST.get('re_pass')
        password=data.user_password
        if Old_Password == password:
            if New_Password == Re_type:
                data.user_password=Re_type
                data.save()
                return render(request,'User/ChangePassword.html',{'msg':"Password Updated"})

            else:
                return render(request,'User/ChangePassword.html',{'msg':"Password Mismatched"})

        else:
            return render(request,'User/ChangePassword.html',{'msg':"Enter Correct Password"})

    return render(request,'User/ChangePassword.html')

def Complaint(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    userid=tbl_user.objects.get(id=request.session['uid'])
    complaintdata=tbl_complaint.objects.filter(user_id=request.session['uid'])
    if request.method == "POST":
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,user_id=userid)
        return render(request,'User/Complaint.html',{'msg':"Inserted"})
    else:   
        return render(request,'User/Complaint.html',{'complaintdata':complaintdata})

def Feedback(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    feedbackdata=tbl_feedback.objects.all()
    userid=tbl_user.objects.get(id=request.session['uid'])
    if request.method=='POST':
        feedback_content=request.POST.get('txt_feedback')
        tbl_feedback.objects.create(user_id=userid,feedback_content=feedback_content)
        return render(request,'User/Feedback.html',{'msg':"Inserted"})
    else:
        return render(request,'User/Feedback.html',{'feedbackdata':feedbackdata})

def logout(request):
    if 'uid' not in request.session:
        return redirect('Guest:Login')
    del request.session['uid']
    return redirect("Guest:Index")

def ViewDeafRequest(request):
    data=tbl_request.objects.filter(user_id=request.session['uid'])
    return render(request,'User/ViewDeafRequest.html',{'data':data})

def rejectdeafrequest(request,rid):
    data=tbl_request.objects.get(id=rid)
    data.request_status=2
    data.save()
    return render(request,'User/ViewDeafRequest.html',{'msg':"Rejected",'rid':rid})

def acceptdeafrequest(request,rid):
    data=tbl_request.objects.get(id=rid)
    data.request_status=1
    data.save()
    return render(request,'User/ViewDeafRequest.html',{'msg':"Accepted",'rid':rid})
from django.http import JsonResponse
from django.db.models import Q

def UserChat(request, did):
    if 'uid' not in request.session:
        return redirect('Guest:Login')

    user = tbl_user.objects.get(id=request.session['uid'])
    deaf = tbl_deafuser.objects.get(id=did)

    if request.method == "POST":
        msg = request.POST.get('msg')
        tbl_chat.objects.create(
            from_user=user,
            to_deaf=deaf,
            message=msg
        )
        return JsonResponse({'status': 'sent'})

    return render(request, 'User/Chat.html', {'deaf': deaf})


def get_messages(request, did):
    user = tbl_user.objects.get(id=request.session['uid'])
    deaf = tbl_deafuser.objects.get(id=did)

    chats = tbl_chat.objects.filter(
        Q(from_user=user, to_deaf=deaf) |
        Q(from_deaf=deaf, to_user=user)
    ).order_by('date')

    data = []
    for c in chats:
        data.append({
            'msg': c.message,
            'type': 'sent' if c.from_user else 'received'
        })

    return JsonResponse(data, safe=False)

import numpy as np
import cv2
import math
from django.shortcuts import render
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# 🔥 Load once
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

labels = ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P",
          "Q","R","S","T","U","V","W","X","Y","SPACE"]

offset = 20
imgSize = 300


def detect_sign_page(request):
    result = None

    if request.method == "POST":
        file = request.FILES.get("image")

        if file:
            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            hands, img = detector.findHands(img)

            final_text = ""   # 🔥 FIX

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal+wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal+hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                final_text = labels[index]

            result = final_text

    return render(request, "User/detect_sign.html", {"result": result})