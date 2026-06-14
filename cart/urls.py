from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart'),
     path('add/', views.add_to_cart, ),
     path('remove/',views.remove_from_cart,),
     path('update/',views.update_quntity),
     path('creat_order/',views.creat_order),
     path("payment_webhook/",views.webhook, name="payment_webhook")

]