from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('list/', views.OrderListAPIView.as_view(), name='order-list'),
    path('status/', views.OrderStatusChoiceAPIView.as_view(), name='order-status'),
    re_path(r"^cancel/(?P<order_number>\d+)/$", views.OrderViewSet.as_view({
        'post': 'order_cancel',
    }), name='order-cancel'),
]