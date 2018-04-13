# -*-coding:utf-8 -*-
from rest_framework import serializers

from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ("user", "goods", "id", )
