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
                  'get_status_display', 'students', 'lessons', 'price', 'discount']

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
