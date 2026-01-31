from django.urls import path
from cart import views

urlpatterns = [
    path('cart/add/',views.add_to_cart,name='add_to_cart'),
    path('cart/update/<int:product_id>/',views.update_cart,name='update_to_cart'),
    path('cart/',views.get_cart,name='get_cart'),
    path('cart/<int:product_id>/',views.remove_from_cart,name='delete_cart'),
    path('cart/filter/',views.filter_item_in_cart,name='filter_cart'),
    path('cart/summary/',views.cart_summary,name='cart_summary'),
    path('cart/clear/',views.clear_cart,name='clear_cart'),
]
