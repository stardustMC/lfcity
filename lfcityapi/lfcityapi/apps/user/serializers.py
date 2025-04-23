from rest_framework import serializers
from user.models import User, UserCourse


class UserCreateModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 're_password', 'phone']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_phone(self, value: str):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError('手机号码不规范!')

        if User.objects.filter(is_active=1, phone=value).exists():
            raise serializers.ValidationError('手机号已存在!')
        return value

    def validate(self, validated_data):
        password = validated_data.get('password', "")
        re_password = validated_data.pop('re_password')

        if password is None or re_password is None:
            raise serializers.ValidationError('密码格式不正确!')

        if password != re_password or not password:
            raise serializers.ValidationError("两次密码不一致或为空!")

        return validated_data

from course.serializers import CourseSerializer
class UserCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'study_time']