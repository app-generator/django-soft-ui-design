# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import WorkerListView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    # path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
    # path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    # path("drivers/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
    # path("drivers/<int:pk>/license_update/", LicenseUpdateView.as_view(), name="license-update"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
