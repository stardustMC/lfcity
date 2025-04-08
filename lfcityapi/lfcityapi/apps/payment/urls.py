from django.urls import path, re_path
from .views import AliPayViewSet


urlpatterns = [
    re_path(r"^alipay/link/(?P<order_number>\d+)/$", AliPayViewSet.as_view({"get": "link"}), name="pay_link"),
    path("alipay/result/", AliPayViewSet.as_view({"get": "pay_feedback"}), name="pay_feedback"),
    re_path(r"^alipay/query/(?P<order_number>\d+)/$", AliPayViewSet.as_view({"get": "query"}), name="pay_query"),
    path("alipay/notify/", AliPayViewSet.as_view({"post": "notify_result"}), name="pay_notify"),
]