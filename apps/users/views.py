# -*-coding:utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


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