from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from DeafUser.models import *
from django.utils import timezone
from datetime import timedelta

def district(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    dis = tbl_district.objects.all()
    if request.method == "POST":
        districtcount = tbl_district.objects.filter(district_name=request.POST.get("dis_txt")).count()
        if districtcount > 0:
            return render(request, 'Admin/district.html', {'msg': "District already exists"})
        else:
            tbl_district.objects.create(district_name=request.POST.get("dis_txt"))
            return redirect("Admin:district")
    return render(request, 'Admin/district.html', {'district': dis})

def delDistrict(request, did):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    tbl_district.objects.get(id=did).delete()
    return redirect("Admin:district")

def editDistrict(request, eid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    editData = tbl_district.objects.get(id=eid)
    if request.method == "POST":
        editData.district_name = request.POST.get('dis_txt')
        editData.save()
        return redirect("Admin:district")
    else:
        return render(request, 'Admin/district.html', {'editData': editData})

def category(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    catg = tbl_category.objects.all()
    if request.method == "POST":
        tbl_category.objects.create(category_name=request.POST.get("cat_txt"))
        return redirect("Admin:category")
    return render(request, 'Admin/Category.html', {'category': catg})


def delcatg(request, cat):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    tbl_category.objects.get(id=cat).delete()
    return redirect("Admin:category")

def ViewFeedback(request):
    data=tbl_feedback.objects.all()
    return render(request,'Admin/Feedback.html',{'data':data})

def editCatg(request, edi):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    editData = tbl_category.objects.get(id=edi)
    if request.method == "POST":
        editData.category_name = request.POST.get('cat_txt')
        editData.save()
        return redirect("Admin:category")
    else:
        return render(request, 'Admin/Category.html', {'editData': editData})


def AdminRegistration(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    reg = tbl_admin.objects.all()
    if request.method == "POST":
        emailcount = tbl_admin.objects.filter(admin_email=request.POST.get("txt_mail")).count()
        if emailcount > 0:
            return render(request, 'Admin/AdminRegistration.html', {'msg': "Email already exists", 'registration': reg})
        else:
            tbl_admin.objects.create(
                admin_name=request.POST.get("txt_name"),
                admin_email=request.POST.get("txt_mail"),
                admin_pass=request.POST.get("txt_pass")
            )
            return redirect("Admin:AdminRegistration")
    return render(request, 'Admin/AdminRegistration.html', {'registration': reg})


def delAdmin(request, adm):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    tbl_admin.objects.get(id=adm).delete()
    return redirect("Admin:AdminRegistration")


def editAdmin(request, dei):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    editData = tbl_admin.objects.get(id=dei)
    if request.method == "POST":
        editData.admin_name  = request.POST.get('txt_name')
        editData.admin_email = request.POST.get('txt_mail')
        editData.admin_pass  = request.POST.get('txt_pass')
        editData.save()
        return redirect("Admin:AdminRegistration")
    else:
        return render(request, 'Admin/AdminRegistration.html', {'editData': editData})


def place(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    districtData = tbl_district.objects.all()
    placeData    = tbl_place.objects.all()
    if request.method == "POST":
        placeName  = request.POST.get('place_txt')
        district   = tbl_district.objects.get(id=request.POST.get('sel_district'))
        placecount = tbl_place.objects.filter(place_name=placeName).count()
        if placecount > 0:
            return render(request, 'Admin/place.html', {'msg': "Place already exists", 'districtData': districtData, 'placeData': placeData})
        else:
            tbl_place.objects.create(place_name=placeName, district=district)
            return redirect("Admin:place")
    return render(request, 'Admin/place.html', {'districtData': districtData, 'placeData': placeData})


def delplace(request, plc):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    tbl_place.objects.get(id=plc).delete()
    return redirect("Admin:place")


def editplace(request, pcl):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    districtData = tbl_district.objects.all()
    editplaceObj = tbl_place.objects.get(id=pcl)
    placeData    = tbl_place.objects.all()
    if request.method == "POST":
        editplaceObj.place_name = request.POST.get('place_txt')
        editplaceObj.district   = tbl_district.objects.get(id=request.POST.get('sel_district'))
        editplaceObj.save()
        return redirect("Admin:place")
    return render(request, 'Admin/place.html', {'districtData': districtData, 'editplace': editplaceObj, 'placeData': placeData})


def SubCategory(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    categoryData    = tbl_category.objects.all()
    subcategoryData = tbl_subcatgory.objects.all()
    if request.method == "POST":
        subCatName = request.POST.get('sub_txt')
        category   = tbl_category.objects.get(id=request.POST.get('select_category'))
        tbl_subcatgory.objects.create(subcatgory_name=subCatName, category=category)
        return redirect("Admin:SubCategory")
    return render(request, 'Admin/SubCategory.html', {'categoryData': categoryData, 'subcategoryData': subcategoryData})


def delsubcategory(request, sid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    tbl_subcatgory.objects.get(id=sid).delete()
    return redirect("Admin:SubCategory")


def editsubcategory(request, cid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    categoryData       = tbl_category.objects.all()
    editsubcategoryObj = tbl_subcatgory.objects.get(id=cid)
    if request.method == "POST":
        editsubcategoryObj.subcatgory_name = request.POST.get('sub_txt')
        editsubcategoryObj.category        = tbl_category.objects.get(id=request.POST.get('select_category'))
        editsubcategoryObj.save()
        return redirect("Admin:SubCategory")
    return render(request, 'Admin/SubCategory.html', {'editsubcategory': editsubcategoryObj, 'categoryData': categoryData})


def HomePage(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    total_users        = tbl_user.objects.count() + tbl_deafuser.objects.count()
    hearing_users      = tbl_user.objects.count()
    deaf_users         = tbl_deafuser.objects.count()
    place_count        = tbl_place.objects.count()
    subcat_count       = tbl_subcatgory.objects.count()
    pending_deaf_count = tbl_deafuser.objects.filter(deafuser_status=0).count()
    complaint_count    = tbl_complaint.objects.filter(complaint_status=0).count()
    total_users_list   = tbl_user.objects.filter()[:5]
    total_deaf_list    = tbl_deafuser.objects.filter()[:5]
    cdata              = tbl_complaint.objects.filter()[:5]
    return render(request, 'Admin/HomePage.html', {
        'total_users':        total_users,
        'hearing_users':      hearing_users,
        'deaf_users':         deaf_users,
        'place_count':        place_count,
        'subcat_count':       subcat_count,
        'pending_deaf_count': pending_deaf_count,
        'complaint_count':    complaint_count,
        'aname':              request.session.get('aname'),
        'udata':              total_users_list,
        'ddata':              total_deaf_list,
        'cdata':              cdata
    })

def User(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    data = tbl_user.objects.filter(user_status=0)
    dataaa = tbl_user.objects.filter(user_status=1)
    datarr = tbl_user.objects.filter(user_status=2)
    return render(request, 'Admin/User.html', {'abcd': data, 'dataaa': dataaa, 'datarr': datarr})

def acceptuser(request, aid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    userdata = tbl_user.objects.get(id=aid)
    userdata.user_status = 1
    userdata.save()
    return redirect("Admin:User")

def rejectuser(request, rid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    userdata = tbl_user.objects.get(id=rid)
    userdata.user_status = 2
    userdata.save()
    return redirect("Admin:User")


def Reply(request, vid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    viewdata = tbl_complaint.objects.get(id=vid)
    if request.method == 'POST':
        viewdata.complaint_reply  = request.POST.get('reply_txt')
        viewdata.complaint_status = 1
        viewdata.save()
        return redirect("Admin:ViewComplaint")
    return render(request, 'Admin/Reply.html', {'viewdata': viewdata})


def ViewComplaint(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    viewData = tbl_complaint.objects.all()
    return render(request, 'Admin/ViewComplaint.html', {'viewData': viewData})


def DeafUser(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    data  = tbl_deafuser.objects.filter(deafuser_status=0)
    dataa = tbl_deafuser.objects.filter(deafuser_status=1)
    datar = tbl_deafuser.objects.filter(deafuser_status=2)
    return render(request, 'Admin/DeafUser.html', {'abcd': data, 'dataa': dataa, 'datar': datar})


def acceptdeafuser(request, aid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    userdata = tbl_deafuser.objects.get(id=aid)
    userdata.deafuser_status = 1
    userdata.save()
    return redirect("Admin:DeafUser")


def rejectdeafuser(request, rid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    userdata = tbl_deafuser.objects.get(id=rid)
    userdata.deafuser_status = 2
    userdata.save()
    return redirect("Admin:DeafUser")


def logout(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    del request.session['aid']
    return redirect("Guest:Index")