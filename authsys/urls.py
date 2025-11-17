from django.urls import path,include
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login/',LoginView.as_view(template_name ='registration/login.html'), name='login'),
    path('register/', views.SignUp_view, name='register'),
    path('profilepage/', views.profile_view, name='userprofile'),
    path('profileedit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    
    ]
