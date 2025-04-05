from django.utils.safestring import mark_safe
from datetime import datetime
from models import models,BaseModel
from stdimage import StdImageField

# Create your models here.
class CourseDirection(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="方向名称")
    remark = models.TextField(default="", blank=True, null=True, verbose_name="方向描述")
    recommend_home_hot = models.BooleanField(default=False, verbose_name="是否推荐到首页新课栏目")
    recommend_home_top = models.BooleanField(default=False, verbose_name="是否推荐到首页必学栏目")
    class Meta:
        db_table = "lf_course_direction"
        verbose_name = "学习方向"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="分类名称")
    remark = models.TextField(default="", blank=True, null=True, verbose_name="分类描述")
    direction = models.ForeignKey("CourseDirection", related_name="category_list", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="学习方向")

    class Meta:
        db_table = "lf_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Course(BaseModel):
    course_type = (
        (0, '付费购买'),
        (1, '会员专享'),
        (2, '学位课程'),
    )
    # level_choices = (
    #     (0, '初级'),
    #     (1, '中级'),
    #     (2, '高级'),
    # )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    # course_cover = models.ImageField(upload_to="course/cover", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_cover = StdImageField(variations={
        'thumb_1080x608': (1080, 608),      # 高清图
        'thumb_540x304': (540, 304),        # 中等比例,
        'thumb_108x61': (108, 61, True),    # 小图(第三个参数表示保持图片质量),
    }, max_length=255, delete_orphans=True, upload_to="course/cover", null=True, verbose_name="封面图片", blank=True)
    course_video = models.FileField(upload_to="course/video", max_length=255, verbose_name="封面视频", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type,default=0, verbose_name="付费类型")
    # level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    description = models.TextField(null=True, blank=True, verbose_name="详情介绍")
    # pub_date = models.DateField(auto_now_add=True, verbose_name="发布日期")
    # period = models.IntegerField(default=7, verbose_name="建议学习周期(day)")
    # attachment_path = models.FileField(max_length=1000, blank=True, null=True, verbose_name="课件路径")
    # attachment_link = models.CharField(max_length=1000, blank=True, null=True, verbose_name="课件链接")
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    lessons = models.IntegerField(default=0, verbose_name="总课时数量")
    # pub_lessons = models.IntegerField(default=0, verbose_name="已更新课时数量")
    price = models.FloatField(verbose_name="课程原价", default=0)
    recommend_home_hot = models.BooleanField(default=False, verbose_name="是否推荐到首页新课栏目")
    recommend_home_top = models.BooleanField(default=False, verbose_name="是否推荐到首页必学栏目")
    direction = models.ForeignKey("CourseDirection", related_name="course_list", on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False, verbose_name="学习方向")
    category = models.ForeignKey("CourseCategory", related_name="course_list", on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False, verbose_name="课程分类")
    teacher = models.ForeignKey("Teacher", related_name="course_list", on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False, verbose_name="授课老师")
    credits = models.IntegerField(default=0, verbose_name="课程可用积分")

    def course_cover_small(self):
        if self.course_cover:
            return mark_safe(f'<img style="border-radius: 0%;" src="{self.course_cover.thumb_108x61.url}">')
        return ""

    course_cover_small.short_description = "封面图片(108x61)"
    course_cover_small.allow_tags = True
    course_cover_small.admin_order_field = "course_cover"

    def course_cover_medium(self):
        if self.course_cover:
            return mark_safe(f'<img style="border-radius: 0%;" src="{self.course_cover.thumb_540x304.url}">')
        return ""

    course_cover_medium.short_description = "封面图片(540x304)"
    course_cover_medium.allow_tags = True
    course_cover_medium.admin_order_field = "course_cover"

    def course_cover_large(self):
        if self.course_cover:
            return mark_safe(f'<img style="border-radius: 0%;" src="{self.course_cover.thumb_1080x608.url}">')
        return ""

    course_cover_large.short_description = "封面图片(1080x608)"
    course_cover_large.allow_tags = True
    course_cover_large.admin_order_field = "course_cover"

    @property
    def discount(self):
        now = datetime.now()
        course_activity_discount = CourseActivityDiscount.objects.filter(
            is_active=True,
            # is_display=True,
            course__id=self.id,
            activity__start_time__lt=now,
            activity__end_time__gt=now,
            discount__is_active=True,
            # discount__is_display=True,
        ).first()

        if not course_activity_discount:
            return {}

        discount = course_activity_discount.discount
        calculation = discount.calculation
        discount_price = None
        # 满减有课程最低价格限制
        if calculation.startswith('-') and self.price >= discount.threshold:
            discount_price = self.price - float(discount.calculation[1:])
        # 折扣比例减有最高价格限制
        elif calculation.startswith('*') and self.price < discount.threshold:
            discount_price = self.price * float(discount.calculation[1:])
        elif calculation == '0':
            discount_price = 0

        return {
            "id": discount.id,
            "name": discount.name,
            # "threshold": discount.threshold,
            "calculation": discount.calculation,
            "price": round(discount_price, 2),
            "expire": int(course_activity_discount.activity.end_time.timestamp() - now.timestamp()), # 活动还剩多长时间结束
        } if discount_price else {}

    class Meta:
        db_table = "lf_course_info"
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

class Teacher(BaseModel):
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )

    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, blank=True, null=True, verbose_name="导师签名")
    # avatar = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师头像")
    avatar = StdImageField(variations={
        'thumb_800x800': (800, 800),  # 'large': (800, 800),
        'thumb_400x400': (400, 400),  # 'medium': (400, 400),
        'thumb_50x50': (50, 50, True),  # 'small': (50, 50, True),
    }, delete_orphans=True, upload_to="teacher", null=True, verbose_name="讲师头像")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "lf_teacher"
        verbose_name = "讲师信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

    def avatar_small(self):
        if self.avatar:
            return mark_safe(f'<img style="border-radius: 100%;" src="{self.avatar.thumb_50x50.url}">')
        return ""

    avatar_small.short_description = "头像信息(50x50)"
    avatar_small.allow_tags = True
    avatar_small.admin_order_field = "avatar"

    def avatar_medium(self):
        if self.avatar:
            return mark_safe(f'<img style="border-radius: 100%;" src="{self.avatar.thumb_400x400.url}">')
        return ""

    avatar_medium.short_description = "头像信息(400x400)"
    avatar_medium.allow_tags = True
    avatar_medium.admin_order_field = "avatar"

    def avatar_large(self):
        if self.avatar:
            return mark_safe(f'<img style="border-radius: 100%;" src="{self.avatar.thumb_800x800.url}">')
        return ""

    avatar_large.short_description = "头像信息(800x800)"
    avatar_large.allow_tags = True
    avatar_large.admin_order_field = "avatar"

class CourseChapter(BaseModel):
    """课程章节"""
    # orders = models.SmallIntegerField(default=1, verbose_name="第几章")
    summary = models.TextField(blank=True, null=True, verbose_name="章节介绍")
    # pub_date = models.DateField(auto_now_add=True, verbose_name="发布日期")
    course = models.ForeignKey("Course", related_name='chapter_list', on_delete=models.CASCADE, db_constraint=False, verbose_name="课程名称")

    class Meta:
        db_table = "lf_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-第%s章-%s" % (self.course.name, self.order, self.name)

class CourseLesson(BaseModel):
    """课程课时"""
    lesson_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频'),
    )

    # orders = models.SmallIntegerField(default=1, verbose_name="第几节")
    lesson_type = models.SmallIntegerField(default=2, choices=lesson_type_choices, verbose_name="课时种类")
    lesson_link = models.CharField(max_length=255, blank=True, null=True, help_text="若是video，填视频地址或者视频id，若是文档，填文档地址", verbose_name="课时链接")
    duration = models.CharField(blank=True, null=True, max_length=32, verbose_name="课时时长")  # 仅在前端展示使用
    # pub_date = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    free_trail = models.BooleanField(default=False, verbose_name="是否可试看")
    recommend = models.BooleanField(default=False, verbose_name="是否推荐到课程列表")
    chapter = models.ForeignKey("CourseChapter", related_name='lesson_list', on_delete=models.CASCADE, db_constraint=False, verbose_name="章节")
    course = models.ForeignKey("Course", related_name="lesson_list", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="课程")

    class Meta:
        db_table = "lf_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class Activity(BaseModel):
    start_time = models.DateTimeField(auto_now=True, verbose_name="开始时间")
    end_time = models.DateTimeField(auto_now=True, verbose_name="结束时间")
    remark = models.CharField(max_length=200, verbose_name="备注信息", default="")
    description = models.CharField(max_length=200, verbose_name="活动介绍", default="")

    class Meta:
        db_table = "lf_activity"
        verbose_name = "促销活动"
        verbose_name_plural = verbose_name

class DiscountType(BaseModel):
    remark = models.CharField(max_length=200, verbose_name="备注信息", default="")

    class Meta:
        db_table = "lf_discount_type"
        verbose_name = "折扣类型"
        verbose_name_plural = verbose_name

class Discount(BaseModel):
    threshold = models.IntegerField(default=0, verbose_name="优惠门槛")
    calculation = models.CharField(default="", max_length=200, verbose_name="折扣公式")
    discount_type = models.ForeignKey(to="DiscountType", verbose_name="折扣类型", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "lf_discount"
        verbose_name = "折扣"
        verbose_name_plural = verbose_name

class CourseActivityDiscount(BaseModel):
    course = models.ForeignKey(to="Course", verbose_name="课程", on_delete=models.DO_NOTHING)
    activity = models.ForeignKey(to="Activity", verbose_name="活动", on_delete=models.DO_NOTHING)
    discount = models.ForeignKey(to="Discount", verbose_name="折扣", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "lf_course_activity_discount"
        verbose_name = "课程参与活动折扣"
        verbose_name_plural = verbose_name
