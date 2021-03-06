# -*-coding:utf-8 -*-

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.conf import settings
import xadmin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from django_shop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, HotSearchsViewset
from users.views import SmscodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset, OrderViewset
from trade.views import AlipayView

# Binding ViewSets to URLs explicitly
# http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
# 配置goods的url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置Categories的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")

# 配置codes 注册验证
router.register(r'codes', SmscodeViewset, base_name="codes")

router.register(r'users', UserViewset, base_name="users")

router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

# 收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

# 留言
router.register(r'messages', LeavingMessageViewset, base_name="messages")

# 收货地址
router.register(r'address', AddressViewset, base_name="address")

# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 订单相关
router.register(r'orders', OrderViewset, base_name="orders")

# 轮播图
router.register(r'banners', BannerViewSet, base_name="banners")
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 商品列表页
    url(r'^', include(router.urls)),

    # 首页
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    # 配置上传文件的访问处理函数
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 登录浏览API认证
    url(r'^api-auth/', include('rest_framework.urls')),

    # 获取给定用户名和密码的令牌, drf自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    # 生成DRF自动文档的配置
    url(r'^docs/', include_docs_urls(title="django_shop")),

    # 支付宝支付返回
    url(r'^alipay/return/', AlipayView.as_view(), name="alipay")

]

# 添加调试工具
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

print(urlpatterns)