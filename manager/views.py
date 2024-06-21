from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import TaskTypeForm
from manager.models import Task, Worker, TaskType


@login_required
def index(request: HttpRequest) -> HttpResponse:
    actual_tasks = Task.objects.filter(is_completed=False).count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    workers = Worker.objects.count()

    context = {
        "actual_tasks": actual_tasks,
        "completed_tasks": completed_tasks,
        "workers": workers
    }

    return render(request, "manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "manager/task_type_create.html"
    form_class = TaskTypeForm
    success_url = reverse_lazy("manager:task-type-list")

