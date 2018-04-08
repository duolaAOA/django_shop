# -*-coding:utf-8 -*-
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法！")

        # 验证码频率限制
        one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)   #  一分钟前
        if VerifyCode.objects.filter(add_time__gt=one_min_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送验证码未超过60s, 请稍后再试！")

        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 help_text="验证码", label="验证码", write_only=True,
                                 error_messages={
                                     "required": "请输入验证码",
                                     "max_length": "请确保验证码长度为4位",
                                     "min_length": "请确保验证码长度为4位",
                                 })
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在！")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_records = verify_records[0]

            five_min_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 5分钟前
            if five_min_ago > last_records.add_time:
                raise serializers.ValidationError("验证码过期！")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误！")

        else:
            raise serializers.ValidationError("验证码错误！")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
