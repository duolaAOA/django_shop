"""django_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin

from django_shop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from goods.views import GoodsListViewSet, CategoryViewSet

# Binding ViewSets to URLs explicitly
# http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
# 配置goods的url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置Categories的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 商品列表页
    url(r'^', include(router.urls)),

    # 配置上传文件的访问处理函数
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 登录浏览API认证
    url(r'^api-auth/', include('rest_framework.urls')),

    # 生成DRF自动文档的配置
    url(r'^docs/', include_docs_urls(title="django_shop"))

]
