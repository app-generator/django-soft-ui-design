from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.home.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.position_admin = Position.objects.create(name="admin")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
            position=self.position_admin
        )
        self.client.force_login(self.admin_user)
        self.position_tester = Position.objects.create(name="tester")
        self.worker = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            position=self.position_tester,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:home_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detailed_position_listed(self):
        url = reverse("admin:home_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

