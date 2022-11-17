# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import WorkerListView, WorkerDetailView, delete_worker, WorkerCreateView, change_task_status, \
    TaskListView, TaskDetailView, TaskCreateView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("<int:pk>", delete_worker, name="worker-delete"),

    path("tasks/", TaskListView.as_view(), name="task-list"),
    # path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    # path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk1>/<int:pk2>", change_task_status, name="change-task-status"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
