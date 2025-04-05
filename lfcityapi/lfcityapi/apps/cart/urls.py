from django.urls import path, re_path

from cart import views

urlpatterns = [
    path('', views.CartAPIView.as_view(), name='cart'),
    path('list/', views.CartSelectedListAPIView.as_view(), name='cart-list'),
]