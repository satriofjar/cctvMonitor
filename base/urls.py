from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cctv/', views.cctv, name='cctv'),
]
