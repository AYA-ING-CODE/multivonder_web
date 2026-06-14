from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from .models import Product


def profile_page(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(
            user=request.user
        )

        return render(request, "profile.html", {
        "products": products})
    else:
        return redirect("login")


def add_product(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        Product.objects.create(
            user=request.user,
            name=request.POST.get("name"),#/نستعو هادا لاننا ستعملنا نوع بيانات مختلف
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            price=request.POST.get("price"),
            image=request.FILES.get("image")
        )

        return JsonResponse({"message": "Product added successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def delete_product(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
      
    if request.method == "DELETE":

        try:
            data = json.loads(request.body)
            product_id = data.get("id")

            product = Product.objects.get(
                id=product_id,
                user=request.user
            )

            product.delete()

            return JsonResponse({
                "message": "Product deleted"
            })

        except Product.DoesNotExist:
            return JsonResponse({ "message": "Product not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request" }, status=400)

def modify_Product(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        try:

            product_id = request.POST.get("id")

            product = Product.objects.get(
                id=product_id,
                user=request.user
            )

            product.name = request.POST.get("name")
            product.description = request.POST.get("description")
            product.category = request.POST.get("category")
            product.price = request.POST.get("price")

            image = request.FILES.get("image")

            if image:
                product.image = image

            product.save()

            return JsonResponse({
                "message": "Product modify successfully"
            })

        except Product.DoesNotExist:
            return JsonResponse({
                "message": "Product not found"
            }, status=404)

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

    return JsonResponse({
        "message": "Invalid request"
    }, status=400)
    





    


        



        
   

 





