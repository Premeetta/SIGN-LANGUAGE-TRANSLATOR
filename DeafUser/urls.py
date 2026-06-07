from django.urls import path 
from DeafUser import views
app_name = "DeafUser"
urlpatterns = [
    path('HomePage/',views.HomePage,name="HomePage"),
    path('MyProfile/',views.MyProfile,name="MyProfile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path('logout/',views.logout,name="logout"),

    #chat
    path('UserList/',views.UserList,name="UserList"),
    path('sendrequest/<int:uid>/',views.sendrequest,name="sendrequest"),
    path('myrequest/',views.myrequest,name="myrequest"),
    path('Complaint/',views.Complaint,name="Complaint"),

    path('chat/<int:uid>/', views.DeafChat, name='chat'),
    path('get-messages/<int:uid>/', views.get_messages_deaf, name='get_messages_deaf'),
    path('sign-message/<int:uid>/', views.sign_message, name='sign_message'),
    path('detect-sign/<int:uid>/', views.detect_sign, name='detect_sign'),

]