from django.urls import path 
from . import views


urlpatterns = [
    path('index/', views.index),
    path('dbtest/', views.db_test),

]