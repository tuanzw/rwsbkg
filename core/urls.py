from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('carriers', views.add_carrier, name='add_carrier'),
    path('check_carrier', views.check_carrier, name='check_carrier'),
    path('list_carrier', views.list_carrier, name='list_carrier'),
    path('delete_carrier/<int:id>', views.delete_carrier, name='delete_carrier'),
    path('edit_carrier/<int:id>', views.edit_carrier, name='edit_carrier'),
    # user feature
    path('users', views.add_user, name='add_user'),
    path('check_username', views.check_username, name='check_username'),
    path('list_user', views.list_user, name='list_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('set_password/<int:id>', views.set_password, name='set_password'),
    # driver feature
    path('drivers', views.add_driver, name='add_driver'),
    path('edit_driver/<int:id>', views.edit_driver, name='edit_driver'),
    path('list_driver', views.list_driver, name='list_driver'),
    # vehicle feature
    path('vehicles', views.add_vehicle, name='add_vehicle'),
    path('edit_vehicle/<int:id>', views.edit_vehicle, name='edit_vehicle'),
    path('list_vehicle', views.list_vehicle, name='list_vehicle'),
    path('toggle_vehicle/<int:id>', views.toggle_vehicle, name='toggle_vehicle'),
]
