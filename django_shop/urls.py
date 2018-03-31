# -*-coding:utf-8 -*-

from django.conf.urls import url, include
# from django.contrib import admin
import xadmin

from django_shop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmscodeViewset

# Binding ViewSets to URLs explicitly
# http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
# 配置goods的url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置Categories的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# 配置codes 注册验证
router.register(r'codes', GoodsListViewSet, base_name="codes")

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

    # 获取给定用户名和密码的令牌, drf自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    # 生成DRF自动文档的配置
    url(r'^docs/', include_docs_urls(title="django_shop"))

]
