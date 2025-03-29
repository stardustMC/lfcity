from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

# Create your views here.
class HomeAPIView(APIView):

    def get(self, request):
        redis = get_redis_connection('default')
        # for i in range(10):
        #     redis.lpush('home', i)
        home = redis.lrange('home', 0, 20)
        return Response(home, status=status.HTTP_200_OK)
