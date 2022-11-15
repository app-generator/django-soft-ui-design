# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import WorkerListView, WorkerDetailView, delete_worker, WorkerCreateView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("<int:pk>", delete_worker, name="worker-delete"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
