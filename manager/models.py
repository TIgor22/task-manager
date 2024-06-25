from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager.settings import AUTH_USER_MODEL


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.position})"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.HIGH
    )
    assignees = models.ManyToManyField(AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ("is_completed", "deadline", )

    def __str__(self) -> str:
        return self.name
