from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import TaskType, Position, Task


class ModelsTests(TestCase):

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_type")
        task = Task.objects.create(
            name="test",
            description="test_description",
            deadline="2024-12-20 18:40",
            is_completed=True,
            task_type=task_type,
            priority="high",
        )
        self.assertEqual(str(task), task.name)

    def test_worker_str(self):
        worker = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position})"
        )

    def test_create_worker_with_position(self):
        position = Position.objects.create(name="test position")
        username = "test_username"
        password = "test123"
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)
