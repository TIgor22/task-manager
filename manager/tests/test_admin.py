from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(
            name="test position"
        )
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=self.position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_add_first_last_position_fields(self):
        url = reverse("admin:manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "position")
