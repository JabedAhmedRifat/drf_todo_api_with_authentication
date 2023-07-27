from django.urls import path
from .views import *



urlpatterns = [
    path('', apiOverview, name="api-overview"),
    path('task-list/', taskList, name="task-list"),
    path('task-detail/<str:pk>/', taskDetail, name="task-Detail"),
    path('task-create/', taskCreate, name="task-Create"),
    path('task-update/<str:pk>/', taskUpdate, name="task-update"),
    path('task-delete/<str:pk>/', taskDelete, name="task-delete"),
]
