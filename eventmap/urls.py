from django.urls import path

from . import views

urlpatterns = [
    path('', views.listMaps, name='listMaps'),
    path('<int:mapid>/', views.listEvents, name='listEvents'),
    path('<int:mapid>/insertEvent/',views.insertEvent,name='insertEvent'),
    path('<int:mapid>/updateEvent/',views.listEvents,name='updateEvent'),
    path('<int:mapid>/detach/',views.detach,name='detach'),
]
