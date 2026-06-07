from django.urls import path
from Basics import views
urlpatterns = [
    path('Sum/',views.Sum),
    path('Largest/',views.Largest),
    path('Calculator/',views.Calculator), 
    
]