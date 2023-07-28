from django.urls import path
from . import views
urlpatterns = [
    path('users/',views.ListUsers.as_view(),name='userdata'), 
    path('login/',views.Loginuser.as_view(),name='login'),
    path('register/',views.Registeruser.as_view(),name='register'),
    path('delete/',views.Deleteuser.as_view(),name='delete'),
]
