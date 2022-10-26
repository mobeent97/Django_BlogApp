from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="HomePage"),
    path('room/<str:pk>/', views.room, name="RoomPage"),
    path('createroom/', views.createRoom, name="CreateRoom"),
    path('updateroom/<str:pk>/', views.updateRoom, name="UpdateRoom"),
    path('profile/<str:pk>/', views.userProfile, name="UserProfile"),
    path('deleteroom/<str:pk>/', views.deleteRoom, name="DeleteRoom"),
    path('deletemessage/<str:pk>/', views.deleteMessage, name="DeleteMessage"),
    path('login/', views.loginpage, name="LoginPage"),
    path('register/', views.registerpage, name="RegisterPage"),
    path('logout/', views.logoutpage, name="LogoutPage"),
    path('updateuser/', views.updateuser, name="UpdateUser"),
    path('topics/', views.gettopics, name="TopicsPage"),
    path('activity/', views.getactivity, name="ActivityPage")
]
