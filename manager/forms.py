from django import forms

from manager.models import TaskType, Position


class TaskTypeForm(forms.ModelForm):

    class Meta:
        model = TaskType
        fields = "__all__"


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = "__all__"

