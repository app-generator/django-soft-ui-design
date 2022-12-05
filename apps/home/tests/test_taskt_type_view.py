from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.models import TaskType, Task, Position

TASK_TYPE_URL = reverse("home:task-type-list")


class PublicTaskTypeTests(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="tester")
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", position=position
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="test1")
        TaskType.objects.create(name="test2")
        res = self.client.get(TASK_TYPE_URL)
        task_types = TaskType.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["tasktype_list"]), list(task_types))
        self.assertTemplateUsed(res, "home/tasktype_list.html")
