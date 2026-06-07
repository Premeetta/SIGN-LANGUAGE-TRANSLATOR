from django.urls import path
from Admin import views
app_name = "Admin"
urlpatterns = [
    path('district/',views.district,name="district"),
    path('delDistrict/<int:did>',views.delDistrict,name="delDistrict"),
    path('editDistrict/<int:eid>',views.editDistrict,name="editDistrict"),
    path('category/',views.category,name="category"),
    path('delcatg/<int:cat>',views.delcatg,name="delcatg"),
    path('editCatg/<int:edi>',views.editCatg,name="editCatg"),
    path('AdminRegistration',views.AdminRegistration,name="AdminRegistration"),
    path('delAdmin/<int:adm>',views.delAdmin,name="delAdmin"),
    path('editAdmin/<int:dei>',views.editAdmin,name="editAdmin"),
    path('place/',views.place,name="place"),
    path('delplace/<int:plc>',views.delplace,name="delplace"),
    path('editplace/<int:pcl>',views.editplace,name="editplace"),
    path('SubCategory/',views.SubCategory,name="SubCategory"),
    path('delsubcategory/<int:sid>',views.delsubcategory,name="delsubcategory"),
    path('editsubcategory/<int:cid>',views.editsubcategory,name="editsubcategory"),

    path('HomePage/',views.HomePage,name="HomePage"),
    path('User/',views.User,name="User"),
    path('ViewFeedback/',views.ViewFeedback,name="ViewFeedback"),
    

    path('acceptuser/<int:aid>',views.acceptuser,name="acceptuser"),
    path('rejectuser/<int:rid>',views.rejectuser,name="rejectuser"),
    path('ViewComplaint/',views.ViewComplaint,name="ViewComplaint"),
    path('Reply/<int:vid>',views.Reply,name="Reply"),
    path('DeafUser/',views.DeafUser,name="DeafUser"),
    
    path('acceptdeafuser/<int:aid>',views.acceptdeafuser,name="acceptdeafuser"),
    path('rejectdeafuser/<int:rid>',views.rejectdeafuser,name="rejectdeafuser"),  
    path('logout/',views.logout,name="logout"), 

   
]