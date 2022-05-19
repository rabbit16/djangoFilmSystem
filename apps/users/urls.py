# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 8:14 下午
# @Author  : rabbit
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from users import views
app_name = 'index'
urlpatterns = [
    path('', views.index.as_view(), name='see_index'),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("session/", views.Session.as_view(), name="session"),
    path("Seat/", views.Seat.as_view(), name="seat")
]
