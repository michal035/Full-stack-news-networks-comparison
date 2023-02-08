from django.urls import path 
from . import views


urlpatterns = [
    path('index/', views.index2),
    path('archive/', views.archive),
    path('archive/<keyword>/', views.archive),
    path('keywords/', views.key_words),
    path('api/', views.api),
    path('api/<keyword>/', views.api),
    path('contact/', views.contact)
 

]