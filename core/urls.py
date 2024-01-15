from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    # path('logout', LogoutView.as_view(), name='logout'),
    path('add_carrier', views.add_carrier, name='add_carrier'),
]
