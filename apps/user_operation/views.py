# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins

from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
        """
        用户收藏功能
        """
        queryset = UserFav.objects.all()
        serializer_class = UserFavSerializer