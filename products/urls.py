from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_page,name='profile'),
    path('add-product/',views.add_product),
    path('delete-product/' ,views.delete_product),
    path('modifyProduct/',views.modify_Product),
]