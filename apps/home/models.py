import os
import uuid

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.utils.text import slugify


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


def worker_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.username)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/workers/", filename)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to=worker_image_file_path)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    @property
    def tasks_assigned_to(self):
        return len(self.tasks.all())

    @property
    def progress(self):
        worker_tasks = self.tasks.all()
        if not worker_tasks:
            return 0
        completed_tasks = 0
        for task in worker_tasks:
            if task.is_completed:
                completed_tasks += 1
        return int(completed_tasks * 100 / self.tasks_assigned_to)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("home:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [(1, "Urgent"), (2, "High"), (3, "Medium"), (4, "Low")]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "priority", "deadline"]

    def get_absolute_url(self):
        return reverse("home:task-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
