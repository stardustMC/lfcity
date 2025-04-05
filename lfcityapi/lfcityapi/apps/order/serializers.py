from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models, transaction
from django_redis import get_redis_connection

from datetime import datetime
from course.models import Course
from order.models import Order, OrderDetail
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
        user_id = self.context['request'].user.id
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

                # 根据id来获取课程列表
                queryset = Course.objects.filter(is_active=True, is_display=True, pk__in=course_id_list).all()
                # 计算实际价格和总价格，并关联课程与订单关系
                total_price, real_price = 0, 0
                order_details = []
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
                # 批量创建订单，提高效率
                OrderDetail.objects.bulk_create(order_details)

                # 为订单补充信息
                order.real_price = real_price
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

                return order
            except Exception as e:
                logger.error(e)
                transaction.rollback(t1)
                raise ValidationError("订单创建失败！")