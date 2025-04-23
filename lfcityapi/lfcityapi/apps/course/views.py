from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from course.models import Course, CourseDirection, CourseCategory
from course.pagination import CourseListPagination
from course.serializers import CourseSerializer, CourseDirectionSerializer, CourseCategorySerializer, \
    CourseDetailSerializer
from user.models import UserCourse
from user.serializers import UserCourseSerializer


# Create your views here.
class CourseDirectionListView(ListAPIView):
    queryset = CourseDirection.objects.filter(is_active=True, is_display=True).order_by('id').all()
    serializer_class = CourseDirectionSerializer
    authentication_classes = ()

class CourseCategoryListView(ListAPIView):
    # queryset = CourseCategory.objects.filter(is_active=True, is_display=True).order_by('id').all()
    serializer_class = CourseCategorySerializer
    authentication_classes = ()

    def get_queryset(self):
        queryset = CourseCategory.objects.filter(is_active=True, is_display=True)

        direction = int(self.kwargs.pop("direction", -1))
        if direction > 0:
            queryset = queryset.filter(direction_id=direction)
        return queryset.order_by('id').all()

class CourseListView(ListAPIView):
    # queryset = Course.objects.filter(is_active=True, is_display=True).order_by('id').all()
    serializer_class = CourseSerializer
    pagination_class = CourseListPagination
    authentication_classes = ()
    filter_backends = [OrderingFilter, ]
    ordering_fields = ('id', 'students', 'order')

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True, is_display=True)
        direction = int(self.kwargs.pop('direction', -1))
        if direction > 0:
            queryset = queryset.filter(direction=direction)
        category = int(self.kwargs.pop('category', -1))
        if category > 0:
            queryset = queryset.filter(category=category)

        return queryset.all()

class CourseRetrieveModelView(RetrieveAPIView):
    queryset = Course.objects.filter(is_active=True, is_display=True).all()
    serializer_class = CourseDetailSerializer
    authentication_classes = ()

class CourseUserListView(CourseListView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserCourseSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = UserCourse.objects.select_related('course').filter(is_active=True, is_display=True, user_id=user_id)

        course_type = int(self.request.query_params.get('type', -1))
        if course_type > -1:
            queryset = queryset.filter(course__course_type=course_type)
        return queryset.all()

class CourseTypeChoiceAPIView(APIView):
    def get(self, request):
        return Response(Course.course_types)


from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter
from .serializers import CourseIndexHaystackSerializer

class CourseSearchViewSet(HaystackViewSet):
    """课程信息全文搜索视图类"""
    # 指定本次搜索的最终真实数据的保存模型
    index_models = [Course]
    serializer_class = CourseIndexHaystackSerializer
    filter_backends = [OrderingFilter, HaystackFilter]
    ordering_fields = ('id', 'students', 'orders')
    pagination_class = CourseListPagination