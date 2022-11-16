# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic

from apps.home.forms import WorkerCreationForm
from apps.home.models import Worker, Task, TaskType


@login_required(login_url="/login/")
def index(request):

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
               'segment': 'index',
               "num_workers": num_workers,
               "num_tasks": num_tasks,
               "num_task_types": num_task_types,
               "num_visits": num_visits,
               }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    # template_name =
    paginate_by = 2


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("home:worker-list")


@login_required
def delete_worker(request, pk):
    worker = Worker.objects.get(id=pk)
    worker.delete()
    return redirect("home:worker-list")


@login_required
def change_task_status(request, pk1, pk2):
    task = Task.objects.get(id=pk1)
    task.is_completed = not task.is_completed
    task.save()
    return redirect(reverse("home:worker-detail", kwargs={'pk': pk2}))

