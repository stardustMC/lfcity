from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .service import get_user_coupons, get_user_enable_coupons


# Create your views here.
class CouponListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.id
        coupons = get_user_coupons(user_id)
        return Response(coupons)


class CouponEnableListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.id
        coupons = get_user_enable_coupons(user_id)
        return Response(coupons)
