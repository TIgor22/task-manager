from django.urls import path

from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("task-types/", views.TaskTypeListView.as_view(), name="task-type-list"),
]

