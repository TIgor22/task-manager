from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Task, TaskType


class PublicTaskTest(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="test_task_type")
        self.task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline="2024-06-28",
            is_completed=True,
            task_type=task_type,
            priority="high",
        )

    def test_login_required_task_list(self):
        url = reverse("manager:task-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_task_detail(self):
        url = reverse("manager:task-detail", kwargs={"pk": self.task.pk})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_task_create(self):
        url = reverse("manager:task-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="test_task_type")
        self.task = Task.objects.create(
            name="test_name",
            description="test_description",
            deadline="2024-06-28",
            is_completed=True,
            task_type=self.task_type,
            priority="high",
        )

    def test_retriv_task_list(self):
        url = reverse("manager:task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/task_list.html")

    def test_retriv_task_detail(self):
        url = reverse("manager:task-detail", kwargs={"pk": self.task.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/task_detail.html")

    def test_retriv_task_create(self):
        url = reverse("manager:task-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/task_form.html")
