
from django.urls import path
from .views import CreateTicketView, AddTaskView, GetCompletionDateView, GetIssueDataView

urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='create_ticket'),
    path('add-task/', AddTaskView.as_view(), name='add_task'),
    path('get-completion-date/', GetCompletionDateView.as_view(), name='get_completion_date'),
    path('get-issue-data/', GetIssueDataView.as_view(), name='get_issue_data'),
]
