import logging
from celery import shared_task
from django.db import transaction

from coupon.service import save_coupon_redis
from order.models import Order

logger = logging.getLogger("django")

@shared_task(name="order_timeout")
def order_timeout(order_id):
    order = Order.objects.filter(id=order_id, is_active=True, is_display=True).first()
    if order.order_status == 0:
        with transaction.atomic():
            s1 = transaction.savepoint()
            try:
                order.order_status = 3
                order.save()

                user_coupon = order.to_coupon.first()
                if user_coupon:
                    save_coupon_redis(user_coupon)

                if order.credits > 0:
                    order.user.credits += order.credits
                    order.user.save()
                return {'order_id': order_id, 'status': True, 'message': "订单超时取消!"}
            except Exception as e:
                logger.error(f"订单超时取消出现错误： {e}")
                transaction.rollback(s1)
                return {'order_id': order_id, 'status': False, 'message': str(e)}