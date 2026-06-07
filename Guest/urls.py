from django.urls import path
from Guest import views
app_name = "Guest"
urlpatterns = [
    path('User/',views.User,name="User"),  
    path('Login/',views.Login,name="Login"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('',views.Index,name="Index"),
    path('DeafUser/',views.DeafUser,name="DeafUser"),
    
    
]