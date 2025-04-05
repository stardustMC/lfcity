from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderCreateSerializer


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)