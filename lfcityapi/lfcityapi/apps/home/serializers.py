from rest_framework import serializers
from home.models import Nav, Banner


class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name', 'is_http', 'link']

class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image', 'is_http', 'link']