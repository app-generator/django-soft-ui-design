from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.home.forms import WorkerCreationForm
from apps.home.models import Position, Worker


class FormsTests(TestCase):
    def test_worker_creation_form_with_position_first_last_name_is_valid(self):
        position = Position.objects.create(name="tester")
        form_data = {
            "username": "new_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test_last",
            "position": position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="tester")
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", position=position
        )
        self.client.force_login(self.user)

    def test_create_worker(self):
        form_data = {
            "username": "new_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test_last",
            "position": 1,
        }

        self.client.post(reverse("home:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position.id, form_data["position"])
