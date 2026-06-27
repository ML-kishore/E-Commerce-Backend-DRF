from django.db import models
from users.models import User
from orders.models import OrderItem,Orders


# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = (
        ('INITIATED','INITIATED'),
        ('SUCCESS','SUCCESS'),
        ('FAILED','FAILED'),
        ('REFUNDED','REFUNDED')
    )
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    order = models.ForeignKey(Orders,on_delete=models.PROTECT,related_name='payments')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(max_length=10,default='INR')
    stripe_payment_intent_id = models.CharField(max_length=255,blank=True,null=True)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='INITIATED')
    raw_response = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s {self.order} - {self.amount}"

    