from rest_framework import serializers

from course.models import Course, CourseDirection, CourseCategory, CourseChapter, CourseLesson


class CourseDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ['id', 'name', 'remark']

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'remark']

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_cover', 'course_cover_small', 'course_cover_large', 'course_video', 'get_course_type_display', 'description',
                  'get_status_display', 'students', 'lessons', 'price', 'discount', 'credits']

class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'order', 'get_lesson_type_display', 'lesson_link', 'duration', 'free_trail']

class CourseChapterSerializer(serializers.ModelSerializer):
    lesson_list = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'order', 'summary', 'lesson_list']

class CourseDetailSerializer(serializers.ModelSerializer):
    chapter_list = CourseChapterSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'course_cover_large', 'course_video', 'get_course_type_display', 'description',
                  'get_status_display', 'students', 'lessons', 'price', 'discount', 'chapter_list']

from drf_haystack.serializers import HaystackSerializer
from .search_indexes import CourseIndex
from django.conf import settings

class  CourseIndexHaystackSerializer(HaystackSerializer):
    """课程搜索的序列化器"""
    class Meta:
        index_classes = [CourseIndex]
        fields = ["text", "id", "name", "course_cover", "get_level_display", "students", "get_status_display", "pub_lessons", "price", "discount", "orders"]

    def to_representation(self, instance):
        """用于指定返回数据的字段的"""
        # 课程的图片，在这里通过elasticsearch提供的，所以不会提供图片地址左边的域名的。因此在这里手动拼接
        instance.course_cover = f'//{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/uploads/{instance.course_cover}'
        return super().to_representation(instance)