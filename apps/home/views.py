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

from apps.home.forms import WorkerCreationForm, TaskCreationForm, TaskUpdateForm, TaskSearchForm, TaskTypeCreationForm
from apps.home.models import Worker, Task, TaskType, Position


@login_required(login_url="/login/")
def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        'segment': 'index',
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_positions": num_positions,
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
    paginate_by = 3


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("home:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 3
    queryset = Task.objects.all().select_related("task_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super(TaskListView, self).get_context_data(**kwargs)
        contex["search_form"] = TaskSearchForm()

        task_type = self.request.GET.get("task_type", "")

        contex["search_form"] = TaskSearchForm(initial={
            "task_type": task_type
        })

        return contex

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                task_type__name__icontains=form.cleaned_data["task_type"]
            )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("home:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("home:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 3
    queryset = TaskType.objects.all()


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreationForm
    success_url = reverse_lazy("home:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 3
    queryset = Position.objects.all()


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


@login_required
def assign_to_task(request, pk):
    current_user = request.user
    if current_user in Task.objects.get(id=pk).assignees.all():
        Task.objects.get(id=pk).assignees.remove(current_user)
    else:
        Task.objects.get(id=pk).assignees.add(current_user)
    return redirect(reverse("home:task-detail", kwargs={'pk': pk}))


@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect("home:task-list")


@login_required
def delete_task_type(request, pk):
    task_type = TaskType.objects.get(id=pk)
    task_type.delete()
    return redirect("home:task-type-list")
