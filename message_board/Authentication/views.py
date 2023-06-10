from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


# Create your views here.

# path('create/', views.create_user, name='create_user'),
# path('login/', views.login_user, name='login_user'),
# path('logout/', views.logout_user, name='logout_user'),
# path('profile/', views.get_user_profile, name='get_user_profile'),
# path('profile/update/', views.update_user_profile, name='update_user_profile'),
# path('profile/delete/', views.delete_user_profile, name='delete_user_profile')

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:

            # username = request.POST.get("username")
            # password = request.POST.get("password")
            # email = request.POST.get("email")
            # first_name = request.POST.get("first_name")
            # last_name = request.POST.get("last_name")

            data = json.loads(request.body)

            username = data.get("username")
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")

            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists", status=400)
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists", status=400)
            

            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name)
            
            json_res = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            }
            return JsonResponse(json_res)
        except Exception as e:
            return HttpResponse("User already exists", status=400)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        data = json.loads(request.body)

        username = data.get("username")

        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            return HttpResponse("User does not exist", status=400)
        
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            json_res = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            }
            return JsonResponse(json_res)
        else:
            return HttpResponse("Invalid credentials", status=400)


def logout_user(request):
    logout(request)
    return HttpResponse("Logout successful")

@csrf_exempt
@login_required
def get_user_profile(request):
    user = request.user
    json_res = {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }
    return JsonResponse(json_res)

@csrf_exempt
@login_required
def update_user_profile(request):
    if request.method == "PUT":
        user = request.user

        data = json.loads(request.body)

        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        new_password = data.get("new_password")


        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if new_password:
            user.set_password(new_password)
        
        user.save()

        return HttpResponse("User profile updated successfully")
    
@csrf_exempt
def delete_user_profile(request):
    if request.method == "DELETE":
        user = request.user
        logout(request)
        user.delete()
        return HttpResponse("User profile deleted successfully")
    else:
        return HttpResponse("Only DELETE requests allowed", status=405)