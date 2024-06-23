from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from manager.models import TaskType, Position, Worker, Task


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


class TaskSearchForm(forms.Form):
    task = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Task"}
        )
    )


class TaskForm(forms.ModelForm):

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
