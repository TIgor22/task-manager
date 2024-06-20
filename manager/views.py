from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from manager.models import Task, Worker


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
