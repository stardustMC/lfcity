from models import BaseModel, models
from course.models import Course, CourseDirection, CourseCategory
from order.models import Order
from user.models import User


# Create your models here.
class Coupon(BaseModel):
    discount_choices = (
        (1, '减免'),
        (2, '折扣'),
    )
    type_choices = (
        (0, '通用类型'),
        (1, '指定方向'),
        (2, '指定分类'),
        (3, '指定课程'),
    )
    # get_choices = (
    #     (0, "系统赠送"),
    #     (1, "自行领取"),
    # )
    discount = models.SmallIntegerField(choices=discount_choices, default=1, verbose_name="优惠方式")
    coupon_type = models.SmallIntegerField(choices=type_choices, default=0, verbose_name="优惠券类型")
    total = models.IntegerField(blank=True, default=50, verbose_name="发放数量")
    left = models.IntegerField(blank=True, default=50, verbose_name="剩余数量")
    start_time = models.DateTimeField(verbose_name="启用时间", null=True, blank=True, default=None)
    end_time = models.DateTimeField(verbose_name="过期时间", null=True, blank=True, default=None)
    # get_type = models.SmallIntegerField(choices=get_choices, default=0, verbose_name="领取方式")
    threshold = models.IntegerField(blank=True, default=0, verbose_name="优惠价格门槛")
    # per_limit = models.SmallIntegerField(default=1, verbose_name="每人限制领取数量")
    calculation = models.CharField(verbose_name="优惠公式", max_length=200, help_text="""
            *号开头表示折扣价，例如*0.82表示八二折；<br>
            -号开头表示减免价,例如-10表示在总价基础上减免10元<br>
            """)

    class Meta:
        db_table = "lf_coupon"
        verbose_name = "优惠券"
        verbose_name_plural = verbose_name

class CouponCourseDirection(models.Model):
    direction = models.ForeignKey(CourseDirection, on_delete=models.DO_NOTHING, related_name='to_coupon', verbose_name="适用课程方向")
    coupon = models.ForeignKey(to='Coupon', on_delete=models.DO_NOTHING, related_name="to_direction", verbose_name="适用优惠券")
    create_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        db_table = "lf_coupon_direction"
        verbose_name = "优惠券与课程方向"
        verbose_name_plural = verbose_name

class CouponCourseCategory(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.DO_NOTHING, related_name='to_coupon', verbose_name="适用课程类别")
    coupon = models.ForeignKey(to='Coupon', on_delete=models.DO_NOTHING, related_name="to_category", verbose_name="适用优惠券")
    create_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        db_table = "lf_coupon_category"
        verbose_name = "优惠券与课程类别"
        verbose_name_plural = verbose_name

class CouponCourse(models.Model):
    coupon = models.ForeignKey(to='Coupon', on_delete=models.DO_NOTHING, related_name="to_course", verbose_name="适用优惠券")
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name="to_coupon", verbose_name="适用课程")
    create_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        db_table = "lf_coupon_course"
        verbose_name = "优惠券与课程"
        verbose_name_plural = verbose_name

class CouponLog(BaseModel):
    status_choices = ((0, "未使用"), (1, "已使用"), (2, "已过期"))
    coupon = models.ForeignKey(to='Coupon', on_delete=models.DO_NOTHING, related_name="to_order", db_constraint=False, verbose_name="优惠券")
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="to_coupon", verbose_name="订单")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="coupon_log", verbose_name="用户")
    status = models.IntegerField(choices=status_choices, default=0, verbose_name="优惠券状态")

    class Meta:
        db_table = "lf_coupon_log"
        verbose_name = "优惠券发放与使用记录"
        verbose_name_plural = verbose_name
