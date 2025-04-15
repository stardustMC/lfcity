from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from order.models import Order
from coupon.models import CouponLog
# from user.models import Credit, UserCourse
from course.serializers import CourseSerializer
from alipaysdk import AliPaySDK
from rest_framework import status
import logging

from user.models import Credit, UserCourse

logger = logging.getLogger("django")

# Create your views here.
class AliPayViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def link(self, request, order_number):
        order = Order.objects.filter(order_number=order_number).first()
        if order is None:
            return Response("订单不存在！", status=status.HTTP_404_NOT_FOUND)
        elif order.order_status > 0:
            return Response("订单已支付或已取消", status=status.HTTP_400_BAD_REQUEST)

        alipay = AliPaySDK()
        link = alipay.page_pay(order_number, order.real_price, order.name)
        return Response({
            "link": link,
            'pay_type': 0,
            'get_pay_type_display': "支付宝"
        }, status=status.HTTP_200_OK)

    def pay_feedback(self, request):
        """支付宝支付结果的同步通知处理"""
        data = request.query_params.dict()  # QueryDict
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            return Response({"message": "通知结果不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order_number = data.get('order_number')
        order = Order.objects.filter(order_number=order_number).first()
        if order is None:
            return Response({"message": "订单不存在！"}, status=status.HTTP_404_NOT_FOUND)

        courses = order.order_courses.all()
        course_list = [item.course for item in courses]
        # 如果订单 未支付，则修改为 已支付
        if order.order_status == 0:
            result = alipay.query(order_number)
            t1 = transaction.savepoint()
            try:
                if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                    user = request.user
                    now = datetime.now()

                    order.pay_time = now
                    order.order_status = 1
                    order.save()
                    # 修改CouponLog记录（标记为已使用）
                    use_coupon = CouponLog.objects.filter(order=order).first()
                    if use_coupon is not None:
                        use_coupon.status = 1
                        use_coupon.save()
                    # 添加积分流水
                    elif order.credits > 0:
                        Credit.objects.create(operation=1, number=order.credits, user=user)
                    # 添加用户已购买的课程
                    user_courses = []
                    for course in course_list:
                        user_courses.append(UserCourse(course=course, user=user))
                    UserCourse.objects.bulk_create(user_courses)
            except Exception as e:
                logger.error(f"订单数据同步过程出错： {e}")
                transaction.rollback(t1)
                return Response({"errmsg": "意料之外的错误发生了！请联系客服处理"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CourseSerializer(course_list, many=True)
        return Response({
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "real_price": order.real_price,
            "courses": serializer.data
        }, status=status.HTTP_200_OK)

    def query(self, request, order_number):
        """主动查询订单支付的支付结果"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]
        courses_list = []
        for course in course_list:
            courses_list.append(UserCourse(course=course, user=order.user))

        if order.order_status == 0:
            # 请求支付宝，查询订单的支付结果
            alipay = AliPaySDK()
            result = alipay.query(order_number)
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        now_time = datetime.now()
                        # 1. 修改订单状态
                        order.pay_time = now_time
                        order.order_status = 1
                        order.save()
                        # 2.1 记录扣除个人积分的流水信息
                        if order.credits > 0:
                            Credit.objects.create(operation=1, number=order.credits, user=order.user)

                        # 2.2 补充个人的优惠券使用记录
                        coupon_log = CouponLog.objects.filter(order=order).first()
                        if coupon_log:
                            coupon_log.use_time = now_time
                            coupon_log.use_status = 1  # 1 表示已使用
                            coupon_log.save()

                        # 3. 用户和课程的关系绑定
                        user_course_list = []
                        for course in course_list:
                            user_course_list.append(UserCourse(course=course, user=order.user))
                        UserCourse.objects.bulk_create(user_course_list)

                        # todo 4. 取消订单超时

                    except Exception as e:
                        logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                        transaction.savepoint_rollback(save_id)
                        return Response({"errmsg": "当前订单支付未完成！请联系客服工作人员！"},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                """当前订单未支付"""
                return Response({"errmsg": "当前订单未支付！"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"errmsg": "当前订单已支付！"})

    def notify_result(self, request):
        """支付宝支付结果的异步通知处理"""
        # drf中接收POST参数需要使用request.data
        data = request.data
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            # 因为是属于异步处理，这个过程无法通过终端调试，因此，需要把支付发送过来的结果，记录到日志中。
            logger.error(f"[支付宝]>> 异步通知结果验证失败：{data}")
            return HttpResponse("fail")

        if data.get("trade_status") not in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
            return HttpResponse("fail")

        # 基于支付包异步请求的支付结果中提取订单号
        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return HttpResponse("fail")
        except Order.DoesNotExist:
            return HttpResponse("fail")

        # 如果已经支付完成，则不需要继续往下处理
        if order.order_status == 1:
            return HttpResponse("success")

        # 获取本次下单的商品课程列表
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]
        courses_list = []

        for course in course_list:
            courses_list.append(UserCourse(course=course, user=order.user))

        """支付成功"""
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                now_time = datetime.now()
                # 1. 修改订单状态
                order.pay_time = now_time
                order.order_status = 1
                order.save()
                # 2.1 记录扣除个人积分的流水信息
                if order.credits > 0:
                    Credit.objects.create(operation=1, number=order.credits, user=order.user)

                # 2.2 补充个人的优惠券使用记录
                coupon_log = CouponLog.objects.filter(order=order).first()
                if coupon_log:
                    coupon_log.use_time = now_time
                    coupon_log.use_status = 1  # 1 表示已使用
                    coupon_log.save()

                # 3. 用户和课程的关系绑定
                user_course_list = []
                for course in course_list:
                    user_course_list.append(UserCourse(course=course, user=order.user))
                UserCourse.objects.bulk_create(user_course_list)

                # todo 4. 取消订单超时

            except Exception as e:
                logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                transaction.savepoint_rollback(save_id)
                return HttpResponse("fail")

        return HttpResponse("success")