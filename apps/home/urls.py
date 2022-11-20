# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import WorkerListView, WorkerDetailView, delete_worker, WorkerCreateView, change_task_status, \
    TaskListView, TaskDetailView, TaskCreateView, assign_to_task

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/delete/<int:pk>/", delete_worker, name="worker-delete"),

    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    # path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/status/<int:pk1>/<int:pk2>/", change_task_status, name="change-task-status"),
    path("tasks/assign/<int:pk>/", assign_to_task, name="assign-to-task"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
