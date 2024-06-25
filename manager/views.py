from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from manager.forms import (
    TaskTypeForm, PositionForm, WorkerForm, TaskSearchForm, TaskForm
)
from manager.models import Task, Worker, TaskType, Position


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


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "manager/position_list.html"
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    template_name = "manager/position_create.html"
    form_class = PositionForm
    success_url = reverse_lazy("manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "manager/worker_detail.html"
    context_object_name = "worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object

        completed_tasks = Task.objects.filter(
            assignees=worker, is_completed=True
        )
        actual_tasks = Task.objects.filter(
            assignees=worker, is_completed=False
        )

        context["actual_tasks"] = actual_tasks
        context["completed_tasks"] = completed_tasks

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = "manager/worker_form.html"
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = "manager/worker_form.html"
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "manager/worker_confirm_delete.html"
    success_url = reverse_lazy("manager:worker-list")


class TaskView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "manager/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskView, self).get_context_data(**kwargs)
        task = self.request.GET.get("task", "")
        context["search_form"] = TaskSearchForm(initial={"task": task})
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        task = self.request.GET.get("task")
        if task:
            return queryset.filter(name__icontains=task)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")
    form_class = TaskForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "manager/task_confirm_delete.html"


class TaskCompletedView(LoginRequiredMixin, generic.View):
    model = Task

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()

        return HttpResponseRedirect(
            reverse("manager:task-detail", kwargs={"pk": pk})
        )
