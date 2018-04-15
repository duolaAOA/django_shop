# -*-coding:utf-8 -*-

from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from .models import VerifyCode
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    重写
    自定义认证
    # http://python.usyiyi.cn/translate/django_182/topics/auth/customizing.html
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # user = Usermodel.objects.get(email=email)
            user = User.objects.get(Q(username=username) | Q(mobile=username))   # 并集查询
        except User.DoesNotExist:
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


class UserViewset(CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication, )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer

        return UserRegisterSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
