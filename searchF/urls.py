from django.urls import path
from . import views

urlpatterns = [
    path('', views.foods_list, name='search'),
]
