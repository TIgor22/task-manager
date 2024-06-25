from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import TaskType


class PublicTypeTaskTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_task_type_list(self):
        url = reverse("manager:task-type-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_task_type_create(self):
        url = reverse("manager:task-type-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTypeTaskTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="QA")
        TaskType.objects.create(name="Refactoring")
        url = reverse("manager:task-type-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/task_type_list.html")

    def test_retrieve_task_type_create(self):
        url = reverse("manager:task-type-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/task_type_create.html")

    def test_redirect_task_type_create_to_success(self):
        url = reverse("manager:task-type-create")
        res = self.client.post(url, {"name": "test_task_type"})
        self.assertRedirects(res, reverse("manager:task-type-list"))
