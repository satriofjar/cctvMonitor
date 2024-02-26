from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cctv/', views.cctv, name='cctv'),
    # path('stream/', views.stream, name='stream'),
    path('stream/', views.camerafeed, name='stream'),
]
