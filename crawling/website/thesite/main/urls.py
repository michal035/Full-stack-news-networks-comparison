from django.urls import path 
from . import views


urlpatterns = [
    path('index/', views.index),
    path('archive/', views.archive),
    path('archive/<number_of_days>/', views.archive),
    path('dbtest/', views.db_test),

]