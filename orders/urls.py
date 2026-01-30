from django.urls import path,include
from . import views
urlpatterns = [
    path('add/', views.place_order, name='place_order'),
    path('cancel/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('get_orders/',views.get_orders,name='orders'),
    path('get_orders/<int:order_id>/',views.get_one_order,name='order'),
    path('status_change/<int:order_id>/', views.update_status,name='update_status'),

]
