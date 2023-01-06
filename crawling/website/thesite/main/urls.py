from django.urls import path 
from . import views


urlpatterns = [
    path('index/', views.index),
    path('archive/', views.archive),
    path('archive/<number_of_months>/', views.archive),
    path('dbtest/', views.db_test),
    path('statistics/', views.statistics)

]