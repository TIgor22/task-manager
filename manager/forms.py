from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import TaskType, Position, Worker


class TaskTypeForm(forms.ModelForm):

    class Meta:
        model = TaskType
        fields = "__all__"


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = "__all__"


class WorkerForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position",)

