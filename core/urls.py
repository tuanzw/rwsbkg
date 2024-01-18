from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('carriers', views.add_carrier, name='add_carrier'),
    path('check_carrier', views.check_carrier, name='check_carrier'),
    path('carriers/<int:id>', views.delete_carrier, name='delete_carrier'),
]
