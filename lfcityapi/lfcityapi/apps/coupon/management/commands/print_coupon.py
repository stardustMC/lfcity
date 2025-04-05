from faker import Faker
from random import randint
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from course.models import Course, CourseDirection, CourseCategory
from coupon.models import Coupon, CouponCourseDirection, CouponCourseCategory, CouponCourse, CouponLog

faker = Faker(["zh-CN"])

class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.course_count = Course.objects.count()
        self.direction_count = CourseDirection.objects.count()
        self.category_count = CourseCategory.objects.count()

    def add_arguments(self, parser):
        parser.add_argument(
            '--kind',
            type=int,
            dest='kind',
            default=50,
            help="要印刷的优惠券种类量",
        )

    def handle(self, *args, **options):
        # 每次循环，都会随机创建一种优惠券，默认每一种优惠券有100张，送完即止
        for i in range(options["kind"]):
            discount = randint(1, 2)
            if discount == 1:
                value = randint(200, 1000)
            else:
                value = randint(50, 99) / 100

            now = datetime.now()
            coupon_type = randint(0, 3)
            coupon = Coupon.objects.create(
                name=faker.job() + " 优惠券",
                discount=discount,
                calculation=('-' if discount == 1 else '*') + str(value),
                coupon_type = coupon_type,
                total = 50,
                left = 50,
                # start_time = now,
                # end_time = now + timedelta(days=30 * 6),
                # get_type = randint(0, 1),
                threshold = value * 2 if discount == 1 else 3000,
                # per_limit = randint(1, 5)
            )
            # course direction specified
            if coupon_type == 1:
                CouponCourseDirection.objects.create(
                    direction_id=randint(1, self.direction_count),
                    # we just printed it
                    coupon_id=coupon.id,
                    create_time=now,
                )
            # course category specified
            elif coupon_type == 2:
                CouponCourseCategory.objects.create(
                    category_id=randint(1, self.category_count),
                    # we just printed it
                    coupon_id=coupon.id,
                    create_time=now,
                )
            # course specified
            elif coupon_type == 3:
                CouponCourse.objects.create(
                    course_id=randint(1, self.course_count),
                    # we just printed it
                    coupon_id=coupon.id,
                    create_time=now,
                )