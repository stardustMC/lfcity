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
            coupon_type = randint(1, 3)
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
                id_range = list(range(1, self.direction_count))
                for _ in range(len(id_range) // 4):
                    CouponCourseDirection.objects.create(
                        direction_id=id_range.pop(randint(0, len(id_range) - 1)),
                        # we just printed it
                        coupon_id=coupon.id,
                        create_time=now,
                    )
            # course category specified
            elif coupon_type == 2:
                id_range = list(range(1, self.category_count))
                for _ in range(len(id_range) // 6):
                    CouponCourseCategory.objects.create(
                        category_id=id_range.pop(randint(0, len(id_range) - 1)),
                        # we just printed it
                        coupon_id=coupon.id,
                        create_time=now,
                    )
            # course specified
            elif coupon_type == 3:
                id_range = list(range(1, self.course_count))
                for _ in range(len(id_range) // 10):
                    CouponCourse.objects.create(
                        course_id=id_range.pop(randint(0, len(id_range) - 1)),
                        # we just printed it
                        coupon_id=coupon.id,
                        create_time=now,
                    )