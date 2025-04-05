from django.urls import path
from . import views

urlpatterns = [
    path("", views.CouponListAPIView.as_view(), name="coupon-list"),
    path("enable/", views.CouponEnableListAPIView.as_view(), name="coupon-enable"),
]