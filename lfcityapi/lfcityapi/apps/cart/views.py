from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from course.serializers import CourseSerializer


# Create your views here.
class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        redis = get_redis_connection('cart')
        user_id = request.user.id
        cart_hash = redis.hgetall("cart_%s" % user_id)

        cart_dict = {int(course.decode()): int(selected.decode()) for course, selected in cart_hash.items()}
        queryset = Course.objects.filter(is_active=True, is_display=True, id__in=cart_dict.keys()).all()
        course_list = []
        for course in queryset:
            course_list.append({
                'id': course.id,
                'name': course.name,
                'course_cover': course.course_cover.url,
                'course_type': course.get_course_type_display(),
                'price': course.price,
                'credits': course.credits,
                'discount': course.discount,
                'selected': cart_dict[course.id],
            })
        return Response({"message": "购物车数据返回成功.", "data": course_list}, status=status.HTTP_200_OK)

    def post(self, request):
        redis = get_redis_connection('cart')
        user_id = request.user.id
        course_id = int(request.data.get('course_id', 0))

        if not Course.objects.filter(pk=course_id).exists():
            return Response({"message": "要添加到购物车中的课程不存在!"}, status=status.HTTP_400_BAD_REQUEST)

        if redis.hexists('cart_%s' % user_id, course_id):
            cart_count = redis.hlen('cart_%s' % user_id)
            return Response({"message": "课程已经在购物车里啦～", "cart_count": cart_count}, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            redis.hset('cart_%s' % user_id, course_id, 1)
            cart_count = redis.hlen('cart_%s' % user_id)
            return Response({"message": "添加到购物车成功～", "cart_count": cart_count}, status=status.HTTP_200_OK)

    def put(self, request):
        redis = get_redis_connection('cart')
        user_id = request.user.id
        course_id = int(request.data.get('course_id', 0))
        selected = int(request.data.get('selected', 0))

        if not Course.objects.filter(pk=course_id).exists():
            return Response({"message": "课程不存在!"}, status=status.HTTP_400_BAD_REQUEST)

        if redis.hexists('cart_%s' % user_id, course_id):
            # print(redis.hget('cart_%s' % user_id, course_id))
            redis.hset('cart_%s' % user_id, course_id, selected)
            # print(redis.hget('cart_%s' % user_id, course_id))
            return Response({"message": "反选操作成功～"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "课程未在购物车内!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        redis = get_redis_connection('cart')
        user_id = request.user.id
        course_id = int(request.query_params.get('course_id', 0))

        if redis.hexists('cart_%s' % user_id, course_id):
            redis.hdel('cart_%s' % user_id, course_id)
            cart_count = redis.hlen('cart_%s' % user_id)
            return Response({"message": "从购物车内删除成功～", "cart_count": cart_count}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "课程已经不在购物车内!"}, status=status.HTTP_400_BAD_REQUEST)

class CartSelectedListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer

    def get_queryset(self):
        redis = get_redis_connection('cart')
        user_id = self.request.user.id
        cart_hash = redis.hgetall("cart_%s" % user_id)

        cart_dict = {int(course.decode()): int(selected.decode()) for course, selected in cart_hash.items() if selected == b'1'}
        queryset = Course.objects.filter(is_active=True, is_display=True, id__in=cart_dict.keys())

        return queryset.all()
