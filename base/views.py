from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

# @api_view(['POST'])
# def reg(request):
#     User.objects.create_user(email=request.data["email"],password=request.data["pwd"],username=request.data["user"],
#     is_staff=1,is_superuser=1)
#     # User.objects.create_user(request.data["usr"],request.data["email"],request.data["pwd"])
#     return HttpResponse ("register")


@api_view(['POST'])
def reg(request):
    # it seems that it is important to rely on the attribute order as it appears in db.sqlite3
    User.objects.create_user(
        request.data["user"], request.data["email"], request.data["pwd"], is_staff=True)
    return HttpResponse('register')
    # User.objects.create(username="foo", password="bar")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mydata(request):
    return HttpResponse("my data....")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['password'] = user.password
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# add new product
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addproduct(request):
    print(request.user)
    desc = request.data['desc']
    price = request.data['price']
    Product.objects.create(desc=desc, price=price, user=request.user)
    return JsonResponse({'POST': "test"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products(request):
    print(request.user)

    # CRUD for authentication
    user = request.user
    res = []  # create an empty list
    for productObj in user.product_set.all():  # run on every row in the table...
            res.append({"desc": productObj.desc,
                        "price": productObj.price,
                        "id": productObj._id
                        })  # append row by to row to res list
    return JsonResponse(res, safe=False)
    # desc =request.data['desc']
    # price =request.data['price']
    # Product.objects.create(desc=desc ,price=price, user=request.user)
    # return JsonResponse({'GEt':"test"})
