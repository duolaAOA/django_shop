# -*-coding:utf-8 -*-
from rest_framework import serializers

from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFav
        fields = ("user", "goods", )
