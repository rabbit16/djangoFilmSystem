# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 8:14 下午
# @Author  : rabbit
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from users import views
app_name = 'index'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("indexTest/", views.IndexTest.as_view(), name="indexTest"),
    path("movie/", views.Movie.as_view(), name="movie"),
    path("rank/", views.Rank.as_view(), name="rank"),
    path("movieDetail/<int:movie_id>/", views.MovieDetail.as_view(), name="movieDetail"),
    # path("movieDetail/", views.MovieDetail.as_view(), name="movieDetail"),
    path("ticket/", views.Ticket.as_view(), name="ticket"),
    path("register/", views.Register.as_view(), name="register"),
    path("session/", views.Session.as_view(), name="session"),
    # path("seats/", views.seats.as_view(), name="seats"),
    path("search/", views.Search.as_view(), name="search"),
    # path("ticketMedium/", views.TicketMedium.as_view(), name="ticketMedium"),
]
