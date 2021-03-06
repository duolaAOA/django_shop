# -*-coding:utf-8-*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .filter import GoodsFilter
from .serializer import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer

# Create your views here.


class GoodsPagination(PageNumberPagination):
    # http://www.django-rest-framework.org/api-guide/pagination/
    # 分页自定制
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页, 分页，搜索，排序
    """
    # 基于mixin实现view
    # generics.ListAPIView 继承 mixins.ListModelMixin,
    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    # http://www.django-rest-framework.org/api-guide/filtering/
    # http://www.django-rest-framework.org/api-guide/filtering/#searchfilter
    queryset = Goods.objects.get_queryset().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'add_time')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    # http://www.django-rest-framework.org/api-guide/generic-views/#retrievemodelmixin
    queryset = GoodsCategory.objects.filter()
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


