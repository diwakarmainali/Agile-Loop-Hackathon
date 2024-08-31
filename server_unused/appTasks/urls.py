from django.urls import path
from .views import (
    prompt_view
)

urlpatterns = [
   
    path('user/add', prompt_view, name='task'),
    #path('get/all-apps/', AllAppsView.as_view(), name='get-apps'),
    #path('user/upload-task/', AddTasksView.as_view(), name='upload_task'),
    
]
