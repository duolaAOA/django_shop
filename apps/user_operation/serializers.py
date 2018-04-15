# -*-coding:utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from .models import UserLeavingMessage, UserAddress
from goods.serializer import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id", )


class UserFavSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods', ),
                message="该商品已经收藏"
            )
        ]
        fields = ("user", "goods", "id", )


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time", )


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
