from faker import Faker
from random import randint
from datetime import datetime, timedelta
from django.core.management import BaseCommand

from user.models import User
from coupon.models import CouponLog, Coupon
from coupon.service import save_coupon_redis

faker = Faker(['zh-CN', 'zh-TW'])
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            type=int,
            dest="amount",
            help="每种优惠券发放的数量",
        )

    def handle(self, *args, **options):
        coupon_count = Coupon.objects.count()
        user_count = User.objects.count()
        for coupon_id in range(1, coupon_count + 1):
            coupon = Coupon.objects.filter(pk=coupon_id).first()
            # 每种优惠券发放amount张，不足则全部发放
            amount = min(coupon.left, options["amount"])

            coupon.left -= amount
            coupon.start_time = datetime.now()
            coupon.end_time = coupon.start_time + timedelta(days=30 * 6)
            coupon.save()
            for i in range(amount):
                instance = CouponLog.objects.create(
                    name=faker.sentence(),
                    user_id=randint(1, user_count),
                    coupon=coupon,
                    # use_time=None,
                    status=0
                )
                save_coupon_redis(instance)