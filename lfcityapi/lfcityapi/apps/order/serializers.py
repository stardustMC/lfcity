from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models, transaction
from django_redis import get_redis_connection

from datetime import datetime

from coupon.models import CouponLog
from course.models import Course
from order.models import Order, OrderDetail
from coupon.service import get_coupon_dict
import json
import logging

logger = logging.getLogger("django")

class OrderCreateSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(max_length=200, default="")

    class Meta:
        model = Order
        fields = ['id', 'pay_type', 'pay_link', 'order_number']
        read_only_fields = ['id', 'order_number']
        extra_kwargs = {
            'pay_type': {'write_only': True},
        }

    def create(self, validated_data):
        redis = get_redis_connection('cart')
        request = self.context.get('request')
        user_id = request.user.id
        cart_hash = redis.hgetall('cart_%s' % user_id)

        with transaction.atomic():
            t1 = transaction.savepoint()
            try:
                # 获取购物车中勾选的商品id列表
                course_id_list = [int(cid.decode()) for cid, select in cart_hash.items() if select == b'1']
                if len(course_id_list) < 1:
                    raise ValidationError("购物车中不存在勾选的商品")
                # 首先创建订单，这样才可以关联订单课程
                # TODO: 这里的订单缺少一些信息（如价格），而支付链接，后续开发完成后补充
                now = datetime.now()
                order = Order.objects.create(
                    user_id=user_id,
                    pay_type=validated_data['pay_type'],
                    # pay_link="",
                    pay_time=now,
                    order_status=0,
                    order_number=now.strftime("%Y%m%d") + "%08d" % user_id + "%08d" % redis.incr("order_number")
                )
                order.pay_link = ""

                # 获取用户使用的优惠方式
                discount_type = request.data.get('discount_type', -1)
                # 优惠券
                coupon_dict, credit = {}, 0
                user_coupon_id = request.data.get('user_coupon_id', 0)
                if discount_type == 0:
                    coupon_dict = get_coupon_dict(user_id, user_coupon_id)
                    if not coupon_dict:
                        raise ValidationError("优惠券数据不存在！")
                # 积分
                elif discount_type == 1:
                    pass

                # 根据id来获取课程列表
                queryset = Course.objects.filter(is_active=True, is_display=True, pk__in=course_id_list).all()
                # 计算实际价格和总价格，并关联课程与订单关系
                total_price, real_price = 0, 0
                order_details = []
                max_discount_price = 0
                for course in queryset:
                    order_details.append(OrderDetail(
                        order=order,
                        course=course,
                        price=course.price,
                        real_price=float(course.discount['price'] if course.discount else course.price),
                        discount_name=course.discount['name'] if course.discount else "",
                    ))
                    real_price += course.discount['price'] if course.discount else course.price
                    total_price += course.price
                    # 已参加其它活动的课程不再适用优惠券或积分
                    if course.discount:
                        continue

                    if coupon_dict:
                        coupon_type = coupon_dict["coupon_type"]
                        # 检查优惠券是否匹配课程
                        coupon_match_course = True
                        if coupon_type == 1:
                            directions = [int(item["direction__id"]) for item in coupon_dict["to_direction"]]
                            coupon_match_course = course.direction_id in directions
                        elif coupon_type == 2:
                            categories = [int(item["category__id"]) for item in coupon_dict["to_category"]]
                            coupon_match_course = course.category_id in categories
                        elif coupon_type == 3:
                            courses = [int(item["course__id"]) for item in coupon_dict["to_course"]]
                            coupon_match_course = course.id in courses

                        if coupon_match_course:
                            threshold = int(coupon_dict["threshold"])
                            # 满减高门槛，折扣低门槛
                            price = 0
                            # 计算最大优惠价格，如果是减免，那就直接是优惠券价格
                            discount = coupon_dict["discount"]
                            if discount == 1 and course.price > threshold:
                                price = float(coupon_dict["calculation"].strip('-'))
                            elif discount == 2 and course.price < threshold:
                                price = float((1 - float(coupon_dict["calculation"].strip('*'))) * course.price)
                            max_discount_price = max(max_discount_price, price)
                    elif credit > 0:
                        pass
                # 批量创建订单，提高效率
                OrderDetail.objects.bulk_create(order_details)

                # 为订单补充信息
                order.real_price = real_price - max_discount_price
                order.total_price = total_price
                order.save()

                # 订单生成后，购物车需要将生成订单的商品（也就是勾选的商品）删除掉
                # 将未勾选的商品记录下来，清空购物车后再加进去
                cart = {cid: select for cid, select in cart_hash.items() if select == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                pipe.delete('cart_%s' % user_id)
                pipe.hset("cart_%s" % user_id, mapping=cart)
                pipe.execute()

                # 也要将用户使用的优惠券一同删除，并更新CouponLog记录
                if max_discount_price > 0:
                    coupon_redis = get_redis_connection('coupon')
                    coupon_redis.delete(f"{user_id}:{user_coupon_id}")

                    CouponLog.objects.filter(pk=user_coupon_id).update(status=1, order=order)

                return order
            except Exception as e:
                logger.error(e)
                transaction.rollback(t1)
                raise ValidationError("订单创建失败！")