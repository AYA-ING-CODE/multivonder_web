from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from .models import Cart, CartItem ,Order, OrderItem
from products.models import Product
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def cart_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()  # related_name="items"
    total = 0
    for item in items:
      total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "items": items,
        "total": total,
     })


#--------------------------------------------------------------------------
def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        data = json.loads(request.body)
        product_id= data.get("id")

        product= Product.objects.get(id=product_id )

        cart, created = Cart.objects.get_or_create( user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({"message": "Added to cart"})

    return JsonResponse({"error": "Invalid request"}, status=400)



#------------------------------------------------------------------------------------
def remove_from_cart(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
      
    if request.method == "DELETE":

        try:
            data = json.loads(request.body)
            item_id = data.get("id")
            cart = Cart.objects.get(user=request.user)

            item = CartItem.objects.get(
                id=item_id,
                cart=cart ,
            )

            item.delete()

            return JsonResponse({
                "message": "Product deleted"
            })

        except CartItem.DoesNotExist:
            return JsonResponse({ "message": "Product not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request" }, status=400)



#-----------------------------------------------------------------------------
def update_quntity(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method != "PUT":
        return JsonResponse({"message": "Method not allowed" }, status=405)

    try:

        data = json.loads(request.body)

        item_id = data.get("item_id")
        quantity = data.get("quantity")
        cart = Cart.objects.get(user=request.user)

        cart_item = CartItem.objects.get(id=item_id , cart=cart)

        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            "message": "updated"
        })

    except CartItem.DoesNotExist:

        return JsonResponse({"message": "Item not found"}, status=404)

    except Exception as e:

        return JsonResponse({ "message": str(e)}, status=400)   

#--------------------------------------------------------------------------------------------------
def creat_order(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed" }, status=405)


    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("cart")

    total_price = 0

    for item in cart_items:
        total_price += item.product.price * item.quantity

    order = Order.objects.create(
        customer=request.user,
        total_price=total_price,
        status="pending",
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            vendor=item.product.user,
            quantity=item.quantity,
            price=item.product.price,
            total_price = item.product.price* item.quantity
        )

    
    # 2. call Chargily-----------------------------------------------------
   
    payload = {
        "amount": float(total_price),
        "currency": "dzd",
        "success_url": "http://127.0.0.1:8000/cart/payment_success/", #ida njah adi l user hna
        "failure_url": "http://127.0.0.1:8000/cart/payment_fail/", #ida fshel  adi l usser hna
        "metadata": {
            "order_reference": order.reference
        },
        "webhook_url": "http://127.0.0.1:8000/cart/payment_webhook/" #hana ahder m3 server 9li ida njah wla lala
    }

    headers = {
        "Authorization": f"Bearer {settings.CHARGILY_SECRET_KEY}",
        "Content-Type": "application/json"
    }
   
    response = requests.post(
        f"{settings.CHARGILY_BASE_URL}/checkouts",
        json=payload,
        headers=headers
    )

    # READ Chargily REPONSE -----------------------------------------------
    if response.status_code != 201:
     return JsonResponse({ "error": response.text}, status=400)
  
    data = response.json()

    # 3. redirect user to payment page--------------------------------------
    checkout_url = data.get("checkout_url")

    return redirect(checkout_url)
 

#--------------------------web hook-------------------
import hashlib
import hmac
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST




@csrf_exempt
@require_POST
def webhook(request):
    # Extracting the 'signature' header from the HTTP request
    signature = request.headers.get('signature')

    # Getting the raw payload from the request body
    payload = request.body.decode('utf-8')

    # If there is no signature, ignore the request
    if not signature:
        return HttpResponse(status=400)

    # Calculate the signature
    # Your Chargily Pay Secret key, will be used to calculate the Signature
    api_secret_key = {settings.CHARGILY_SECRET_KEY}
    computed_signature = hmac.new(api_secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()

    # If the calculated signature doesn't match the received signature, ignore the request
    if not hmac.compare_digest(signature, computed_signature):
        return HttpResponse(status=403)

    # If the signatures match, proceed to decode the JSON payload
    event = json.loads(payload)

    # Switch based on the event type
    if event.get("type") == 'checkout.paid':
        # Handle the successful payment
        data = event.get("data")
        order_reference = data.get("metadata").get("order_reference")
        try:
            order = Order.objects.get(reference=order_reference)
            if order.status != "paid": 
              order.status = "paid"
              order.save()
              user= order.customer
              cart = Cart.objects.get(user=user)
              cart_items = cart.items.all()
              cart_items.delete()

        except Order.DoesNotExist:
            pass

    elif event['type'] == 'checkout.failed':
        checkout = event['data']
        # Handle the failed payment.

    # Respond with a 200 OK status code to let us know that you've received the webhook
    return JsonResponse({}, status=200)





# test mode  = https://pay.chargily.net/test/api/pay-v2
#seting.py ----------------------------------------------------
#CHARGILY_SECRET_KEY = "sk_test_xxxxxxxxxxxxx"
#CHARGILY_BASE_URL = "https://pay.chargily.net/test/api/v2"









