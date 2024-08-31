

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .jira_client import JiraClient
from .ai_client import AIClient
from .serializers import TicketSerializer, TaskSerializer, IssueKeySerializer

JIRA_SERVER = 'tj should do this one'
JIRA_USERNAME = 'djpapzin do this'
JIRA_API_TOKEN = 'djpapzin do this'
AI_API_URL = 'ai api url'
AI_API_KEY = 'put the ai api key'

jira_client = JiraClient(JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN)
ai_client = AIClient(AI_API_URL, AI_API_KEY)

class CreateTicketView(APIView):
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            ticket = jira_client.create_ticket(data['project_key'], data['summary'], data['description'], data['issue_type'])
            return Response(ticket.raw, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddTaskView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            task = jira_client.add_task(data['issue_key'], data['summary'], data['description'])
            return Response(task.raw, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCompletionDateView(APIView):
    def post(self, request):
        serializer = IssueKeySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            completion_date = jira_client.get_completion_date(data['issue_key'])
            return Response({'completion_date': completion_date}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetIssueDataView(APIView):
    def post(self, request):
        serializer = IssueKeySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            issue_data = jira_client.get_issue_data(data['issue_key'])
            return Response(issue_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
