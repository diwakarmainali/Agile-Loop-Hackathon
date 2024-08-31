from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import json
from django.shortcuts import get_object_or_404
from .models import App, CompletedTask
from jira import JIRA
import google.generativeai as genai
import environ
import os
from pathlib import Path
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
import requests
from google.api_core import exceptions as google_exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
from typing import List, Dict, Any
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize Google Gemini client
gemini_model = genai.GenerativeModel('gemini-1.5-flash',
                                     generation_config={"response_mime_type": "application/json"})

def get_jira_client():
    jira_options = {'server': f"https://{env('JIRA_DOMAIN')}.atlassian.net"}
    jira = JIRA(options=jira_options, basic_auth=(env('EMAIL'), env('JIRA_API_KEY')))
    
    return jira




@api_view(['POST'])
@permission_classes([AllowAny])
def prompt_view(request):
    print('noo')
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt')

        # Define the schema for the task creation
        #schema = '{ "summary": str, "description": str, "project_key": str, "issue_type": str }'
        gemini_prompt = f"""
        Analyze the prompt by user [{prompt}] to create a complete jira task object  called data and a single
        Analyze the following user prompt and determine the which action that user want to use:
            
        {prompt}
            
        Respond with a JSON object containing the action and data.
        
        Valid actions are:
            - "create"
            - "assign"
            - "get issues"
            - "fetch_database"
            - "fetch_page"
            -"create_page"
             
        Return a json object only. If the action is create then the data object should have the fields project,
        summary ,description and issue issuetype.if the action is assign then the data objects should be 
        issue, and assignee.If the action is get issues then it should the field project.if the action is
        fetch_database then the data should have database_id and if action is fetch_page then the 
        data should have page_id.If action is create page then the data should have page_id, title and paragraph
        """

        # Use Google Gemini to process the prompt
        response = gemini_model.generate_content(
            gemini_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
            )
        task_info = json.loads(response.text)
        # res= JsonResponse({'data':task_info})
        # automate_jira_task(res)
        print(task_info)
        
        # Automate the Jira task and get the result
        result = automate_jira_task(task_info)
        
        return JsonResponse(result)
    

# Automate Jira task based on the data provided
def automate_jira_task(data):
    jira = get_jira_client()
    task_data = data['data']
    
    # Determine the action to take
    action = data.get('action') or data.get('actionObject', {}).get('action')
    result = {}
    print(action,'action')
    
    if action == 'create':
        result = create_jira_issue(jira, task_data)
    elif action == 'assign':
        result = assign_jira_issue(jira, task_data['issue'], task_data['assignee'])
    elif action == 'get issues':
        result = get_issues(jira, task_data['project'])
    elif action == 'fetch_database':
        result = fetch_databases(task_data['database_id'])
    elif action == 'fetch_page':
        result = fetch_pages(task_data['page_id'])
    elif action == 'create_page':
        result = create_notion_page(task_data['page_id'],env("NOTION_API_KEY"),task_data['title'],task_data['paragraph'])
    else:
        print("No action detected")
    
    return result

# Create a new Jira issue
def create_jira_issue(jira, issue_data)-> Dict[str, Any]:
    #print(get_developer_suggestions(2),'synapse')
    
    issue_dict = {
        'project': issue_data['project'],
        'summary': issue_data['summary'],
        'description': issue_data['description'],
        'issuetype': {'name': 'Task'},
    }
    
    print(issue_dict)
    new_issue = jira.create_issue(fields=issue_dict)
   
    return {'status': 'success', 'message': f"Issue Created: {new_issue.key}", 'issue_key': new_issue.key, 'summary': new_issue.fields.summary,}

# Assign a Jira issue to a user
def assign_jira_issue(jira, issue_key, assignee):
    issue = jira.issue(issue_key)
    issue.update(fields={'assignee': {'name': assignee}})
    return {'status': 'success', 'message': f"Issue {issue_key} assigned to {assignee}"}

# Get issues for a specific project
def get_issues(jira, project_key):
    issues = jira.search_issues(f'project={project_key}')
    issues_list = [{'key': issue.key, 'summary': issue.fields.summary} for issue in issues]
    print(issues_list,"ISSUES")
    return {'status': 'success', 'issues': issues_list}



#==============================================================================================
#Notion
NOTION_BASE_URL = "https://api.notion.com/v1"

DEFAULT_NOTION_HEADERS = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + env("NOTION_API_KEY")
}

def fetch_databases(databaseId: str) -> Dict[str, Any]:
    url = NOTION_BASE_URL + "/databases/" + databaseId
    payload = {}
    response = requests.request("GET", url, headers=DEFAULT_NOTION_HEADERS, data=payload)

    return json.loads(response.text)

def fetch_pages(pageId: str) -> Dict[str, Any]:
    url = NOTION_BASE_URL + "/pages/" + pageId
    payload = {}
    response = requests.request("GET", url, headers=DEFAULT_NOTION_HEADERS, data=payload)

    return json.loads(response.text)

def create_notion_page(page_id: str, notion_api_key: str, title: str, paragraph: str):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": { "page_id": page_id },
        "properties": {
            "title": {
                "title": [{ "type": "text", "text": { "content": title } }]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{ "type": "text", "text": { "content": paragraph } }]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    return json.loads(response.text)
    
# class AddAppView(generics.CreateAPIView):
#     queryset = App.objects.all()
#     serializer_class = AppSerializer
#     permission_classes = [IsAdminUser]

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)


# class AllAppsView(generics.ListAPIView):
#     queryset = App.objects.all()
#     serializer_class = AppSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


# class AddTasksView(generics.CreateAPIView):
#     queryset = CompletedTask.objects.all()
#     serializer_class = AddCompletedTaskSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         app_id = self.request.data.get('appId')
#         app = App.objects.get(id=app_id)
#         serializer.save(user=self.request.user, app=app)


# class UserTasksView(generics.ListCreateAPIView):
#     serializer_class = CompletedTaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Filter the tasks to include only those completed by the authenticated user
#         return CompletedTask.objects.filter(user=self.request.user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         # Serialized data for tasks
#         # Serialized data for user
#         tasks_data = serializer.data  
#         user_data = UserSerializer(self.request.user).data

#         # Construct final response with tasks and user object
#         response_data = {
#             'user': user_data,
#             'tasks': tasks_data
#         }
#         return Response(response_data)


# class AdminTasksView(generics.ListCreateAPIView):
#     serializer_class = CompletedTaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Filtered the tasks to include only those completed by the authenticated user
#         return CompletedTask.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data)


# class VerifyCompletedTaskView(generics.UpdateAPIView):
#     queryset = CompletedTask.objects.all()
#     serializer_class = CompletedTaskUpdateSerializer
#     permission_classes = [permissions.IsAdminUser]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()

#         if not request.user.is_staff:
#             return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

#         # Set the verified field to True
#         serializer = self.get_serializer(
#             instance, data={'verified': True}, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         # Check if the task is verified and credit points to the user
#         if instance.verified:
#             instance.user.user_points += instance.app.points
#             instance.user.save()

#         return Response(serializer.data)
