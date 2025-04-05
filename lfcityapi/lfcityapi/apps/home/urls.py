from django.urls import path
from home import views

urlpatterns = [
    # path('', views.HomeAPIView.as_view(), name='home'),
    path('header/', views.NavHeadListView.as_view(), name='nav_header'),
    path('footer/', views.NavFooterListView.as_view(), name='nav_footer'),
    path('banner/', views.BannerListView.as_view(), name='banner'),
]