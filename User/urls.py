from django.urls import path
from User import views
app_name = "User"
urlpatterns = [
    path('HomePage/',views.HomePage,name="HomePage"),  
    path('MyProfile/',views.MyProfile,name="MyProfile"),
    path('EditProfile/',views.EditProfile,name="EditProfile"),
    path('ChangePassword/',views.ChangePassword,name="ChangePassword"),
    path('Complaint/',views.Complaint,name="Complaint"),  
    path('Feedback/',views.Feedback,name="Feedback"),  
    path('logout/',views.logout,name="logout"),

    #mainlogic
    path('ViewDeafRequest/',views.ViewDeafRequest,name="ViewDeafRequest"),
    path('acceptdeafrequest/<int:rid>/',views.acceptdeafrequest,name="acceptdeafrequest"),
    path('rejectdeafrequest/<int:rid>/',views.rejectdeafrequest,name="rejectdeafrequest"),

    path('chat/<int:did>/', views.UserChat, name='chat'),
    path('get-messages/<int:did>/', views.get_messages, name='get_messages'),

    path('detect-sign/', views.detect_sign_page, name='detect_sign_page'),
]