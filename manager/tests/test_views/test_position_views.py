from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Position


class PublicPositionTest(TestCase):
    def test_login_required_position_list(self):
        url = reverse("manager:position-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create_position(self):
        url = reverse("manager:position-create")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retriv_position_list(self):
        Position.objects.create(name="QA")
        Position.objects.create(name="Designer")
        url = reverse("manager:position-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/position_list.html")

    def test_retriv_position_create(self):
        url = reverse("manager:position-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "manager/position_create.html")

    def test_redirect_to_all_positions_on_success(self):
        url = reverse("manager:position-create")
        res = self.client.post(url, {"name": "test_position"})
        self.assertRedirects(res, reverse("manager:position-list"))
