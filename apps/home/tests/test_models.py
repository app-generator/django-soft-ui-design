from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.home.models import Position, Task, TaskType


class ModelsTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="tester")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        position = Position.objects.create(name="tester1")
        worker = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="first",
            last_name="last",
            position=position,
        )
        self.assertEqual(
            str(worker), f"{worker.username} ({worker.first_name} {worker.last_name})"
        )

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test")
        task = Task.objects.create(
            name="test",
            is_completed=True,
            description="",
            priority=1,
            task_type=task_type,
        )
        self.assertEqual(str(task), task.name)

    def test_create_worker_with_position(self):
        position = Position.objects.create(name="tester2")
        worker = get_user_model().objects.create_user(
            username="test", password="test12345", position=position
        )
        self.assertEqual(worker.username, "test")
        self.assertTrue(worker.check_password("test12345"))
        self.assertEqual(worker.position, position)
