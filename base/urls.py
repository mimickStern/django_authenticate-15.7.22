from . import views
#from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    # Signin/Login
    path('login/', views.MyTokenObtainPairView.as_view(), name="login"), # django's inate login function
    
    # signup/register
    path('register/', views.reg, name="register"),


    path('mydata/', views.mydata, name="mydata"),

    # data add
    path('addproduct/', views.addproduct, name="add"),

    # get all products
    path('products/', views.products, name="getall")
    
]
