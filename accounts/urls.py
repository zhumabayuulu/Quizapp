from django.urls import path
from .views import *
app_name = 'users'
urlpatterns = [
    path('register', SignupView.as_view(), name='register'),
    path("login/", Login.as_view(), name="login"),
    path('profile/<str:username>', ProfailView.as_view(), name='profile'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    path('logout/',logout_user,name='logout'),
]