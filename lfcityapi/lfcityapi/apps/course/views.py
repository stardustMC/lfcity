from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import Course, CourseDirection, CourseCategory
from course.pagination import CourseListPagination
from course.serializers import CourseSerializer, CourseDirectionSerializer, CourseCategorySerializer, \
    CourseDetailSerializer


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