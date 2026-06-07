from django.shortcuts import render,redirect
from Admin.models import*
from Guest.models import*

def User(request):
    district=tbl_district.objects.all() #select
    if request.method == "POST": #buttonclick
        photo = request.FILES.get('txt_photo')
        name = request.POST.get('txtname')
        email = request.POST.get('mail')
        password = request.POST.get('passwd')
        address = request.POST.get('address')
        contact = request.POST.get('txt_contact')
        place = tbl_place.objects.get(id=request.POST.get('sel_place'))
        emailcount=tbl_user.objects.filter(user_email=email).count()
        if emailcount>0:
            return render(request,'Guest/Login.html',{'msg': " email already exist"})  
        else:
            tbl_user.objects.create(user_name=name,user_email=email,user_password=password,user_address=address,user_photo=photo,place=place,user_contact=contact) #insert

            return render(request,'Guest/Login.html',{'msg': " details inserted"})  
    else:
        return render(request,'Guest/User.html',{'districtData':district}) #select

def Login(request):
    if request.method == "POST": #buttonclick
        email=request.POST.get('txt_mail') #variable
        password=request.POST.get('txt_pass') #variable

        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        deafusercount=tbl_deafuser.objects.filter(deafuser_email=email,deafuser_password=password).count()

        admincount=tbl_admin.objects.filter(admin_email=email,admin_pass=password).count()

        if usercount>0:
            userdata=tbl_user.objects.get(user_email=email,user_password=password)
            request.session['uid']=userdata.id
            return redirect('User:HomePage')

        
        elif deafusercount>0:
            deafuserdata=tbl_deafuser.objects.get(deafuser_email=email,deafuser_password=password)
            request.session['duid']=deafuserdata.id
            return redirect('DeafUser:HomePage')

        elif admincount>0:
            admindata=tbl_admin.objects.get(admin_email=email,admin_pass=password)
            request.session['aid']=admindata.id
            request.session['aname']=admindata.admin_name
            return redirect('Admin:HomePage')
        else:
            return render(request,'Guest/Login.html',{'msg':"Invalid Login"})
    else:  
        return render(request,'Guest/Login.html')



# Create your views here.

def ajaxplace(request):
    place = tbl_place.objects.filter(district=request.GET.get('did'))
    return render(request,"Guest/AjaxPlace.html",{'place':place})

def Index(request):
    return render(request,'Guest/Index.html')

def DeafUser(request):
    district=tbl_district.objects.all() #select
    if request.method == "POST": #buttonclick
        photo = request.FILES.get('txt_photo')
        name = request.POST.get('txtname')
        email = request.POST.get('mail')
        password = request.POST.get('passwd')
        address = request.POST.get('address')
        contact = request.POST.get('txt_contact')
        place = tbl_place.objects.get(id=request.POST.get('sel_place'))
        emailcount=tbl_deafuser.objects.filter(deafuser_email=email).count()
        if emailcount>0:
            return render(request,'Guest/DeafUser.html',{'msg': " email already exist"})  
        else:
            tbl_deafuser.objects.create(deafuser_contact=contact,deafuser_name=name,deafuser_email=email,deafuser_password=password,deafuser_address=address,deafuser_photo=photo,place=place) #insert
            return render(request,'Guest/Login.html',{'msg': " details inserted"})  
    else:
        return render(request,'Guest/DeafUser.html',{'districtData':district}) #select