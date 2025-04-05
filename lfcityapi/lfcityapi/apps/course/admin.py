from django.contrib import admin

from course.models import CourseCategory, CourseDirection, Course


# Register your models here.
class CourseCategoryInline(admin.StackedInline):
    model = CourseCategory
    fields = ('name', 'remark')

class CourseDirectionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'recommend_home_hot', "recommend_home_top"]
    list_filter = ['recommend_home_hot', "recommend_home_top"]
    ordering = ['id']
    search_fields = ['name']
    # 内嵌外键
    inlines = [CourseCategoryInline]

admin.site.register(CourseDirection, CourseDirectionModelAdmin)

class CourseCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark']
    ordering = ['id']
    search_fields = ['name']

admin.site.register(CourseCategory, CourseCategoryModelAdmin)

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course_cover_small', 'get_course_type_display', 'description', 'get_status_display',
                    'recommend_home_hot', "recommend_home_top", "get_direction_name", "get_category_name"]
    list_filter = ["direction_id", "category_id"]
    ordering = ['id']
    search_fields = ['name']
    list_per_page = 10
    list_select_related = ['direction', 'category']

    @admin.display(ordering='direction__name', description="课程方向")
    def get_direction_name(self, obj):
        return obj.direction.name if obj.direction else '-'

    @admin.display(ordering='category__name', description="课程分类")
    def get_category_name(self, obj):
        return obj.category.name if obj.category else '-'

admin.site.register(Course, CourseModelAdmin)