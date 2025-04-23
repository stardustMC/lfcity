from django.urls import path, re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('search', views.CourseSearchViewSet, basename='course-search')

urlpatterns = [
    path('directions/', views.CourseDirectionListView.as_view(), name='course-direction-list'),
    re_path(r'^categories/(?P<direction>-?\d+)/$', views.CourseCategoryListView.as_view(), name='course-category-list'),
    re_path(r'^(?P<direction>-?\d+)/(?P<category>-?\d+)/$', views.CourseListView.as_view(), name='course-list'),
    re_path(r'^detail/(?P<pk>\d+)/$', views.CourseRetrieveModelView.as_view(), name='course-detail'),
    path('list/', views.CourseUserListView.as_view(), name='course-user-list'),
    path('types/', views.CourseTypeChoiceAPIView.as_view(), name='course-type-list'),
] + router.urls