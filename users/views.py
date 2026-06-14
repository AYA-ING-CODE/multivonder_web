from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from products.models import Product

def login_view(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"})
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request,
        username=data["usernam"],
        password=data["password"]
    )

    if user is not None:
        login(request, user)  # 🔥 session cookie يتصايب تلقائياً
        return JsonResponse({"message": "logged in"})
    return JsonResponse({"error": "invalid credentials"})
 

def register_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"})

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("usernam")  # نفس اسمك في frontend
    password = data.get("password")

    # 🔴 check if user exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    user = User.objects.create_user(
        username=username,
        password=password
    )
    login(request, user)
    return JsonResponse({"message": "user created"})
    
def home(request):
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        return redirect("login")

def login_page(request):
    return render(request, "login.html")      

def home_page(request):
    if request.user.is_authenticated:
        products = Product.objects.all

        return render(request, "Home.html", {
        "products": products})
    else:
        return redirect("login")



