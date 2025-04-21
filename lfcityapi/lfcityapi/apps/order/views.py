import logging
from django.db import transaction
from coupon.service import save_coupon_redis

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from order.models import Order
from order.pagination import OrderListPagination
from order.serializers import OrderCreateSerializer, OrderSerializer

logger = logging.getLogger("django")

# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

class OrderStatusChoiceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(Order.status_choices)

class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = OrderListPagination
    ordering = ['id', 'update_time']

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user_id=user_id, is_active=True, is_display=True)

        status = int(self.request.query_params.get('status', -1))
        if status > -1:
            queryset = queryset.filter(order_status=status)

        return queryset.all()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def order_cancel(self, request, order_number=None, *args, **kwargs):
        order_number = self.kwargs.get('order_number')
        if not order_number:
            return Response({"message": "订单号不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(order_number=order_number, is_active=True, is_display=True).first()
        if order is None:
            return Response({"message": "订单号错误！"}, status=status.HTTP_400_BAD_REQUEST)

        if order.order_status > 0:
            return Response({"message": "订单已支付或已取消！"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            s1 = transaction.savepoint()
            try:
                order.order_status = 2
                order.save()

                user_coupon = order.to_coupon.first()
                if user_coupon:
                    save_coupon_redis(user_coupon)

                if order.credits > 0:
                    order.user.credits += order.credits
                    order.user.save()
            except Exception as e:
                logger.error(f"订单取消出现错误： {e}")
                transaction.rollback(s1)
                return Response({"message": "出现未知错误！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "订单已成功取消"}, status=status.HTTP_200_OK)
