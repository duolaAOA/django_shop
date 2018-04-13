# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserFavSerializer