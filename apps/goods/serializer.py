# -*-coding:utf-8 -*-

from rest_framework import serializers

from goods.models import Goods, GoodsCategory


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    三层嵌套是做商品目录结构的层次划分
    many=True  表示有多个
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/tutorial/1-serialization/#using-modelserializers
    # 模型管理自动填充映射，与自定定制model一样的，更简单
    category = CategorySerializer()     # 嵌套将category字段嵌入

    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = "__all__"


