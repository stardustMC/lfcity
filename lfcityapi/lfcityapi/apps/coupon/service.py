import json
from datetime import datetime

from course.models import Course
from coupon.models import CouponLog
from django_redis import get_redis_connection


def save_coupon_redis(obj: CouponLog):
    redis = get_redis_connection("coupon")
    if obj.status == 0:
        coupon = obj.coupon
        pipe = redis.pipeline()
        pipe.multi()
        pipe.hset(f"{obj.user.id}:{obj.id}", "coupon_id", coupon.id)
        pipe.hset(f"{obj.user.id}:{obj.id}", "name", coupon.name)
        pipe.hset(f"{obj.user.id}:{obj.id}", "discount", coupon.discount)
        pipe.hset(f"{obj.user.id}:{obj.id}", "get_discount_display", coupon.get_discount_display())
        pipe.hset(f"{obj.user.id}:{obj.id}", "coupon_type", coupon.coupon_type)
        pipe.hset(f"{obj.user.id}:{obj.id}", "get_coupon_type_display", coupon.get_coupon_type_display())
        pipe.hset(f"{obj.user.id}:{obj.id}", "start_time", coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
        pipe.hset(f"{obj.user.id}:{obj.id}", "end_time", coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
        # pipe.hset(f"{obj.user.id}:{obj.id}", "get_type", coupon.get_type)
        # pipe.hset(f"{obj.user.id}:{obj.id}", "get_get_type_display", coupon.get_get_type_display())
        pipe.hset(f"{obj.user.id}:{obj.id}", "threshold", coupon.threshold)
        pipe.hset(f"{obj.user.id}:{obj.id}", "calculation", coupon.calculation)
        pipe.hset(f"{obj.user.id}:{obj.id}", "to_direction",
                  json.dumps(list(coupon.to_direction.values("direction__id", "direction__name"))))
        pipe.hset(f"{obj.user.id}:{obj.id}", "to_category",
                  json.dumps(list(coupon.to_category.values("category__id", "category__name"))))
        pipe.hset(f"{obj.user.id}:{obj.id}", "to_course",
                  json.dumps(list(coupon.to_course.values("course__id", "course__name"))))
        # 设置当前优惠券的有效期
        pipe.expire(f"{obj.user.id}:{obj.id}", int(coupon.end_time.timestamp() - datetime.now().timestamp()))
        pipe.execute()
    else:
        redis.delete(f"{obj.user.id}:{obj.id}")

def get_user_coupons(user_id: int):
    redis = get_redis_connection("coupon")
    keys = redis.keys(f"{user_id}:*")

    user_coupon_keys = [item.decode() for item in keys]
    coupons = []
    for user_coupon in user_coupon_keys:
        coupon_hash = redis.hgetall(user_coupon)

        coupon_item = {"user_coupon_id": int(user_coupon.split(":")[-1])}
        for key, value in coupon_hash.items():
            key = key.decode()
            value = value.decode()
            if key in ('to_direction', 'to_category', 'to_course'):
                value = json.loads(value)
            coupon_item[key] = value
        coupons.append(coupon_item)

    return coupons

def get_user_enable_coupons(user_id: int):
    redis = get_redis_connection('cart')
    cart_hash = redis.hgetall('cart_%s' % user_id)
    course_id_list = [int(course_id.decode()) for course_id, select in cart_hash.items() if select == b'1']

    cart_courses = Course.objects.filter(id__in=course_id_list).all()
    # queryset = CouponLog.objects.filter(user_id=user_id, status=0).all()
    coupons = get_user_coupons(user_id)

    avail_coupons = []
    # 外层循环每一张优惠券
    for coupon in coupons:
        coupon["enable_courses"] = []
        for course in cart_courses:
            # 若课程已经参加了其它优惠活动，禁止使用优惠券（不存在折上折）
            if course.discount:
                continue
            # 指定方向可用
            if coupon["coupon_type"] == '1' and course.direction_id not in [item["direction__id"] for item in coupon["to_direction"]]:
                continue
            # 指定分类可用
            elif coupon["coupon_type"] == '2' and course.category_id not in [item["category__id"] for item in coupon["to_category"]]:
                continue
            # 指定课程可用
            elif coupon["coupon_type"] == '3' and course.id not in [item["course__id"] for item in coupon["to_direction"]]:
                continue

            # 检查优惠门槛
            # 1. 减免的门槛必须低于课程价格 2. 折扣的门槛必须高于课程价格
            if coupon["discount"] == '1' and course.price < int(coupon["threshold"]):
                continue
            if coupon["discount"] == '2' and course.price > int(coupon["threshold"]):
                continue

            avail_coupons.append(coupon)
    return avail_coupons
