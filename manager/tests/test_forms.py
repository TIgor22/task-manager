from django.test import TestCase

from manager.forms import WorkerForm, TaskSearchForm
from manager.models import Position


class FormTests(TestCase):
    def test_worker_creation_form_with_position_first_last_name(self):
        position = Position.objects.create(name="QA")
        form_data = {
            "username": "new_user",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position,
            "password1": "user123test",
            "password2": "user123test"
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_task_search_form(self):
        form = TaskSearchForm()
        self.assertTrue("task" in form.fields)
        self.assertTrue(form.fields["task"].required is False)
        self.assertTrue(form.fields["task"].widget.attrs["placeholder"])
