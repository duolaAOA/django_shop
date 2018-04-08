# -*-coding:utf-8 -*-

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token


User = get_user_model()
"""
信号 http://www.django-rest-framework.org/api-guide/authentication/
"""


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()


