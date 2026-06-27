from rest_framework.response import Response
from .models import Payment
from users.models import User
from orders.models import Orders,OrderItem
from rest_framework.decorators import api_view,permission_classes
from catalog.permissions import IsAdminorReadOnly
from rest_framework.permissions import IsAdminUser,IsAuthenticated
import stripe
from django.conf import settings


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request,order_id):
    order = Orders.objects.get(id=order_id,user=request.user)

    if order.is_cancelled:
        return Response({"error" : "Order has cancelled already..."},status=400)
    
    if hasattr(order,'payment'):
        return Response({"error" : "Payment already done...."},status=400)
    
    paymentintent = stripe.PaymentIntent.create(
        amount = int(order.amount) * 100,
        currency='inr',
        metadata={
            'user_id' : request.user.id
            'order_id' : order.id
        }
    )

    Payment.objects.create(
        user = request.user,
        order = order,
        stripe_payment_intent_id = paymentintent.id
        status = 'INITIATED'
    )

    return Response(
        {"client_secret" : paymentintent.client_secret,"publishable_key" : settings.STRIPE_PUBLISHABLE_KEY},
        status=200
    )