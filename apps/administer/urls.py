# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 12:05 上午
# @Author  : rabbit
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from administer import views
app_name = 'admin'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('film/', views.filmPublish.as_view(), name='film')
]