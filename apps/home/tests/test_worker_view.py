from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.models import Worker, Position

WORKER_URL = reverse("home:worker-list")


class PublicWorkerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="tester")
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        position = Position.objects.create(name="tester1")
        Worker.objects.create(username="test1", password="test1", position=position)
        res = self.client.get(WORKER_URL)
        workers = Worker.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["worker_list"]), list(workers))
        self.assertTemplateUsed(res, "home/main_worker_list.html")
