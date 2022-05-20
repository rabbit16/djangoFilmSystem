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
    path("index_test/", views.Index_test.as_view(), name="index_test"),
    path("movie/", views.Movie.as_view(), name="movie"),
    path("rank/", views.Rank.as_view(), name="rank"),
    path("movieDetail/", views.MovieDetail.as_view(), name="movieDetail"),
    path("ticket/", views.Ticket.as_view(), name="ticket"),
]
