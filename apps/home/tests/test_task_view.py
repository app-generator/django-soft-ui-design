from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.models import TaskType, Task, Position

TASK_URL = reverse("home:task-list")


class PublicTaskTests(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="tester")
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", position=position
        )
        self.client.force_login(self.user)

    def test_retrieve_tasks(self):
        task_type = TaskType.objects.create(name="test")
        Task.objects.create(
            name="test1", is_completed=1, priority=1, task_type=task_type
        )
        Task.objects.create(
            name="test2", is_completed=1, priority=1, task_type=task_type
        )
        res = self.client.get(TASK_URL)
        tasks = Task.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["task_list"]), list(tasks))
        self.assertTemplateUsed(res, "home/main_task_list.html")
