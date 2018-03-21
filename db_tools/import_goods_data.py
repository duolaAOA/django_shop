# -*-coding:utf-8 -*-

import sys
import os
"""
数据导入数据库
"""

pwd = os.path.dirname(os.path.realpath(__file__))   # 当前文件运行路径
sys.path.append(pwd + '../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_shop.settings")

import django

django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    # category_name = goods_detail["categorys"][-1]
    # categories = GoodsCategory.objects.filter(name=category_name)     # 如果取值为空返回空数组
    # # django.db.utils.IntegrityError: (1048, "Column 'category_id' cannot be null")
    # # https://stackoverflow.com/questions/46911907/django-db-utils-integrityerror-1048-column-category-id-cannot-be-null
    # if categories.exists():
    #     category = categories[0]
    # else:
    #     category = GoodsCategory.objects.create(name=category_name)
    # goods.category = category
    # goods.save()
    category_name = goods_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    """
        也可如下
        category, created = GoodsCategory.objects.get_or_create(name=category_name)
        goods.category = category
    """
    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
