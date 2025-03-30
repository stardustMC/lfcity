from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from .serializers import NavModelSerializer
from .models import Nav
import constants

# Create your views here.
class HomeAPIView(APIView):

    def get(self, request):
        redis = get_redis_connection('default')
        for i in range(10):
            redis.lpush('home', i)
        home = redis.lrange('home', 0, 20)
        return Response(home, status=status.HTTP_200_OK)


class NavHeadListView(ListAPIView):
    queryset = Nav.objects.filter(is_active=True, is_display=True, position=constants.NAV_HEAD_POSITION).all()
    serializer_class = NavModelSerializer


class NavFooterListView(ListAPIView):
    queryset = Nav.objects.filter(is_active=True, is_display=True, position=constants.NAV_FOOT_POSITION).all()
    serializer_class = NavModelSerializer