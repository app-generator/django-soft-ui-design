# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_then_login, name="logout"),
]
