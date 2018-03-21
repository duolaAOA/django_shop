# -*-coding:utf-8 -*-

# 独立使用djaogno model

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


from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat["code"]
    lev1_instance.name = lev1_cat["name"]
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev1_cat["code"]
        lev2_instance.name = lev1_cat["name"]
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance
        lev2_instance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat["code"]
            lev3_instance.name = lev3_cat["name"]
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance
            lev3_instance.save()