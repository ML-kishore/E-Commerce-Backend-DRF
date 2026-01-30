from django.urls import path
from cart import views

urlpatterns = [
    path('cart/add/',views.add_to_cart,name='add_to_cart'),
    path('cart/update/<int:product_id>/',views.update_cart,name='update_to_cart'),
    path('cart/',views.get_cart,name='get_cart'),
    path('cart/<int:product_id>/',views.remove_from_cart,name='delete_cart')
]
