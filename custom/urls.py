
from django.urls import path
from custom import views
urlpatterns = [
    path('upload',views.detect_objects,name='upload'),
   
]