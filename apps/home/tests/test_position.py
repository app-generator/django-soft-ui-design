from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.models import Position

POSITION_URL = reverse("home:position-list")


class PublicPositionTests(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTests(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="tester")
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", position=position
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        Position.objects.create(name="tester1")
        Position.objects.create(name="tester2")
        res = self.client.get(POSITION_URL)
        positions = Position.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["position_list"]), list(positions))
        self.assertTemplateUsed(res, "home/main_position_list.html")
