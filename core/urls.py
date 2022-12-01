# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls"))]  # Auth routes - login / register
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Media files routes
urlpatterns += [path("", include(("apps.home.urls", "apps.home"), namespace="home"))]  # Leave `Home.Urls` as the last
# line
