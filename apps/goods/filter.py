# -*-coding:utf-8 -*-

from django_filters.rest_framework import FilterSet
import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(FilterSet):
    """
    商品过滤类
    """
    # https://django-filter.readthedocs.io/en/master/guide/rest_framework.html#quickstart
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    # name = django_filters.CharFilter(name="name", lookup_expr='icontains')  # 模糊查询，加i表示忽略大小写
    # 模糊查询使用drf中的searchfilter替代
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        """
        参数默认传递
        对二级分类的过滤
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value)
                               | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']
