from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),


    path('dashboard', views.dashboard, name='dashboard'),


    path('foods/', views.foods_list, name='foods_list'),
    path('food/add/', views.food_create, name='food_create'),
    path('food/<int:pk>/edit/', views.food_update, name='food_update'),
    path('food/<int:pk>/delete/', views.food_delete, name='food_delete'),


    # path('meals/', views.meals_list, name='food_list'),
    path('meals/add/', views.meal_create, name='meal_create'),
    # path('meals/<int:pk>/delete/', views.meal_delete, name='meal_delete'),
    # path("meals/<int:meal_id>/edit/", views.meal_edit, name="meal_edit"),

    path('daily-kcal/', views.daily_kcal_summary, name='daily_kcal_summary'),
    # detail view uses year/month/day so links are pretty and RESTful
    path('daily-kcal/<int:year>/<int:month>/<int:day>/', views.daily_kcal_detail, name='daily_kcal_detail'),

    path('update/', views.update_weight, name='update_weight'),
    path('history/', views.weight_history, name='weight_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)