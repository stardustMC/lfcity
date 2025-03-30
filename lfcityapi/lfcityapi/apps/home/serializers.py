from rest_framework import serializers
from home.models import Nav


class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name', 'is_http', 'link']
