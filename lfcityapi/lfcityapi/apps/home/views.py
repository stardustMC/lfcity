import constants
from .models import Nav, Banner
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import NavModelSerializer, BannerModelSerializer

# Create your views here.
class CacheListAPIView(ListAPIView):

    @method_decorator(cache_page(constants.LIST_PAGE_CACHE_TIME))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# TODO: 缓存了视图，那么在其他地方更改了数据源（例如admin站点）之后需要考虑删除缓存
class NavHeadListView(CacheListAPIView):
    queryset = Nav.objects.filter(is_active=True, is_display=True, position=constants.NAV_HEAD_POSITION).all()
    serializer_class = NavModelSerializer

class NavFooterListView(CacheListAPIView):
    queryset = Nav.objects.filter(is_active=True, is_display=True, position=constants.NAV_FOOT_POSITION).all()
    serializer_class = NavModelSerializer

class BannerListView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True, is_display=True).all()
    serializer_class = BannerModelSerializer
