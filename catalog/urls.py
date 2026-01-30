from django.urls import path,include
from catalog import views

urlpatterns = [
    path('add_category/',views.create_categories,name='add_category'),
    path('categories/',views.view_categories,name='categories'),
    path('products/',views.view_products,name='view_products'),
    path('products/<int:prod_id>/',views.view_product,name='view_product'),
    path('add_product/',views.add_products,name='add_product')
    
]



