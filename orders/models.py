from django.db import models
from users.models import User
from catalog.models import Products,Categories
from cart.models import Cart,CartItem

# Create your models here.
class Orders(models.Model):

    order_choices = (('order_placed','ORDER_PLACED'),('shipped','SHIPPED'),('out_for_delivery','OUT_FOR_DELIVERY'),('delivered','DELIVERED'))
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='user_order')
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(default='order_placed',max_length=20)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_cancelled = models.BooleanField(default=False)
 

    def __str__(self):
        return f"{self.user}-orderno-{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='orderitem')
    product = models.ForeignKey(Products,on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10,decimal_places=2)

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity
    