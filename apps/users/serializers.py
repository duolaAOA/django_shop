# -*-coding:utf-8 -*-
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
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
