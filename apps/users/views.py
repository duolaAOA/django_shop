# -*-coding:utf-8 -*-

from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import SmsSerializer
from .models import VerifyCode
from utils.yunpian import YunPian


class CustomBackend(ModelBackend):
    """
    重写
    自定义认证
    # http://python.usyiyi.cn/translate/django_182/topics/auth/customizing.html
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        Usermodel = get_user_model()
        try:
            # user = Usermodel.objects.get(email=email)
            user = Usermodel.objects.get(Q(username=username) | Q(mobile=username))   # 并集查询
        except Usermodel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class SmscodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字验证码
        """
        seeds = "0123456789"
        random_str = ''
        for i in range(4):
            random_str += choice(seeds)

        return random_str

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(settings.API_KEY)

        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile,)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"],
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 短信发送成功后保存验证码
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()

            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED
            )

