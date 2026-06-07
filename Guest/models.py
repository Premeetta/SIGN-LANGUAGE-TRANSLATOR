from django.db import models
from Admin.models import *

# Create your models here.

class tbl_user(models.Model):
    user_photo = models.FileField(upload_to="Assets/User/Photo/")
    user_name = models.CharField(max_length=30) 
    user_email = models.CharField(max_length=30)
    user_contact = models.CharField(max_length=10)
    user_address = models.CharField(max_length=30)
    user_password = models.CharField(max_length=8)
    user_status = models.IntegerField(default=0)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    

class tbl_deafuser(models.Model):
    deafuser_photo = models.FileField(upload_to="Assets/DeafUser/Photo")
    deafuser_name = models.CharField(max_length=30)
    deafuser_email = models.CharField(max_length=30)
    deafuser_contact = models.CharField(max_length=30,null=True)
    deafuser_address =  models.CharField(max_length=30)
    deafuser_password = models.CharField(max_length=8)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    deafuser_status = models.IntegerField(default=0)


     