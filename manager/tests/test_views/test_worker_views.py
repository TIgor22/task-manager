from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Worker, Position, Task, TaskType


class PublicWorkerTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(
            username="test_worker",
            password="test123"
        )

    def test_login_required_worker_list(self):
        url = reverse("manager:worker-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_worker_detail(self):
        url = reverse("manager:worker-detail", kwargs={"pk": self.worker.pk})
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_worker_create(self):
        url = reverse("manager:worker-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user123"
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="test_position")
        self.worker = Worker.objects.create(
            username="test_username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            position=self.position,
        )
        task_type = TaskType.objects.create(name="test_task_type")
        self.actual_task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline="2024-06-27",
            is_completed=False,
            task_type=task_type,
            priority="high",
        )
        self.actual_task.assignees.add(self.worker)
        self.actual_task.save()
        self.completed_task = Task.objects.create(
            name="test_task1",
            description="test_description",
            deadline="2024-06-27",
            is_completed=True,
            task_type=task_type,
            priority="medium",
        )
        self.completed_task.assignees.add(self.worker)
        self.completed_task.save()

    def test_retriv_worker_list(self):
        url = reverse("manager:worker-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/worker_list.html")

    def test_retriv_worker_detail(self):
        url = reverse("manager:worker-detail", kwargs={"pk": self.worker.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/worker_detail.html")

    def test_task_in_worker_detail_context(self):
        url = reverse("manager:worker-detail", kwargs={"pk": self.worker.pk})
        res = self.client.get(url)
        self.assertTrue(self.actual_task in res.context["actual_tasks"])
        self.assertTrue(self.completed_task in res.context["completed_tasks"])

    def test_retriv_worker_create(self):
        url = reverse("manager:worker-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/worker_form.html")
