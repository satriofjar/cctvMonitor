from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:pk>/', views.floor_cctv, name='list-cctv'),
    path('cctv/<str:id_floor>/<str:id_camera>/', views.cctv, name='cctv'),
    # path('stream/', views.stream, name='stream'),
    path('stream/<str:pk>/', views.camerafeed, name='stream'),
    path('thumbnail/<str:pk>/', views.show_thumbnail, name='show_thumbnail'),
]
