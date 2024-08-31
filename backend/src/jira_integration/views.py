# import requests
# import os
# from typing import List, Dict, Any
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Jira API base URL
# BASE_URL = f"https://{os.getenv('JIRA_DOMAIN')}.atlassian.net/rest/api/3"

# # Authentication
# EMAIL = os.getenv("EMAIL")
# JIRA_API_KEY = os.getenv("JIRA_API_KEY")
# AUTH = (EMAIL, JIRA_API_KEY)

# # Headers
# HEADERS = {
#     "Accept": "application/json",
#     "Content-Type": "application/json"
# }

# def view_issues(project_key: str) -> List[Dict[str, Any]]:
#     """Retrieve all issues for a given project."""
#     url = f"{BASE_URL}/search"
#     params = {
#         "jql": f"project={project_key}",
#         "fields": "summary,description,status"
#     }
#     response = requests.get(url, headers=HEADERS, auth=AUTH, params=params)
#     response.raise_for_status()
#     return response.json()["issues"]

# def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
#     """Create a new issue in the specified project."""
#     url = f"{BASE_URL}/issue"
#     payload = {
#         "fields": {
#             "project": {"key": project_key},
#             "summary": summary,
#             "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]},
#             "issuetype": {"name": issue_type}
#         }
#     }
#     response = requests.post(url, headers=HEADERS, auth=AUTH, json=payload)
#     response.raise_for_status()
#     return response.json()

# def get_all_users() -> List[Dict[str, Any]]:
#     """Retrieve all users in the Jira instance."""
#     url = f"{BASE_URL}/users/search"
#     response = requests.get(url, headers=HEADERS, auth=AUTH)
#     response.raise_for_status()
#     return response.json()

# def create_user(email: str, display_name: str) -> Dict[str, Any]:
#     """Create a new user in the Jira instance."""
#     url = f"{BASE_URL}/user"
#     payload = {
#         "emailAddress": email,
#         "displayName": display_name
#     }
#     response = requests.post(url, headers=HEADERS, auth=AUTH, json=payload)
#     response.raise_for_status()
#     return response.json()

# def add_file_attachment(issue_key: str, file_path: str) -> Dict[str, Any]:
#     """Add a file attachment to a specific issue."""
#     url = f"{BASE_URL}/issue/{issue_key}/attachments"
#     headers = {**HEADERS, "X-Atlassian-Token": "no-check"}
#     with open(file_path, "rb") as file:
#         files = {"file": file}
#         response = requests.post(url, headers=headers, auth=AUTH, files=files)
#     response.raise_for_status()
#     return response.json()

# def get_issue_comments(issue_key: str) -> List[Dict[str, Any]]:
#     """Retrieve all comments for a specific issue."""
#     url = f"{BASE_URL}/issue/{issue_key}/comment"
#     response = requests.get(url, headers=HEADERS, auth=AUTH)
#     response.raise_for_status()
#     return response.json()["comments"]

# def add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
#     """Add a comment to a specific issue."""
#     url = f"{BASE_URL}/issue/{issue_key}/comment"
#     payload = {
#         "body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment}]}]}
#     }
#     response = requests.post(url, headers=HEADERS, auth=AUTH, json=payload)
#     response.raise_for_status()
#     return response.json()

# def edit_comment(issue_key: str, comment_id: str, updated_comment: str) -> Dict[str, Any]:
#     """Edit an existing comment on a specific issue."""
#     url = f"{BASE_URL}/issue/{issue_key}/comment/{comment_id}"
#     payload = {
#         "body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": updated_comment}]}]}
#     }
#     response = requests.put(url, headers=HEADERS, auth=AUTH, json=payload)
#     response.raise_for_status()
#     return response.json()

# def get_issue_status(issue_key: str) -> str:
#     """Retrieve the status of a specific issue."""
#     url = f"{BASE_URL}/issue/{issue_key}?fields=status"
#     response = requests.get(url, headers=HEADERS, auth=AUTH)
#     response.raise_for_status()
#     return response.json()["fields"]["status"]["name"]

# jira_automation/jira_integration/views.py
import requests
import json
import os
import io
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import logging
from .llm_utils import handle_prompt, view_issues, get_issue_comments, add_comment, edit_comment, get_issue_status

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Setup Jira & Connect Rest API
@csrf_exempt
def setup_jira(request):
    url = "https://lfanampe.atlassian.net/rest/api/2/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    auth = (email, api_key)

    payload = json.dumps({
        "fields": {
            "project": {
                "key": "ALH"
            },
            "summary": "Test1",
            "description": "Testing the Jira Rest API",
            "issuetype": {
                "name": "Task"
            }
        }
    })

    response = requests.post(url, headers=headers, data=payload, auth=auth)

    return JsonResponse({'response': response.text})

# Create Users In Jira From Rest API Using Python
@csrf_exempt
def create_user(request):
    base_url = "https://lfanampe.atlassian.net/rest/api/3"
    user_url = f"{base_url}/user"
    products_url = f"{base_url}/products"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    auth = (email, api_key)

    def redact_email(email):
        parts = email.split('@')
        if len(parts) == 2:
            return f"{'*' * len(parts[0])}@{parts[1]}"
        return email

    def get_available_products():
        try:
            response = requests.get(products_url, headers=headers, auth=auth)
            if response.status_code == 200:
                products = response.json()
                product_keys = [product['key'] for product in products]
                return product_keys
            else:
                logger.error(f"Failed to retrieve products. Status code: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error occurred while retrieving products: {str(e)}")
            return []

    available_products = get_available_products()

    with io.open("userlist.csv", "r", encoding="utf-8") as f1:
        user_data = f1.read().splitlines()[1:]

    responses = []
    for user in user_data:
        user_fields = user.split(",")
        if len(user_fields) < 3:
            logger.warning(f"Skipping invalid user data: {user}")
            continue

        displayname = user_fields[0].strip()
        pwd = user_fields[1].strip()
        email = user_fields[2].strip()
        name = email.split("@")[0]

        payload = json.dumps({
            "password": pwd,
            "emailAddress": email,
            "displayName": displayname,
            "name": name,
            "products": [{"key": key, "access": "LICENSED"} for key in available_products],
            "notification": False
        })

        try:
            response = requests.post(user_url, headers=headers, data=payload, auth=auth)
            responses.append({
                'email': redact_email(email),
                'response': response.text
            })
        except Exception as e:
            responses.append({
                'email': redact_email(email),
                'error': str(e)
            })

    return JsonResponse({'responses': responses})

# How To Add File Attachment
@csrf_exempt
def add_file_attachment(request):
    url = "https://lfanampe.atlassian.net/rest/api/3/issue/ALH-4/attachments"
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    files = {
        "file": ("userlist.csv", open("userlist.csv", "rb"))
    }

    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    auth = (email, api_key)

    response = requests.post(url, headers=headers, files=files, auth=auth)
    return JsonResponse({'response': response.text})

# How To Add Comment To Jira Issue
@csrf_exempt
def add_comment(request):
    url = "https://lfanampe.atlassian.net/rest/api/3/issue/ALH-4/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "This is a comment added by Python script",
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    })

    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    auth = (email, api_key)

    response = requests.post(url, headers=headers, data=data, auth=auth)
    return JsonResponse({'response': response.text})

# How To Edit Existing Comment
@csrf_exempt
def edit_comment(request):
    url = "https://lfanampe.atlassian.net/rest/api/3/issue/ALH-4/comment/10002"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "comment3 edited by python",
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    })

    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    auth = (email, api_key)

    response = requests.put(url, headers=headers, data=data, auth=auth)
    return JsonResponse({'response': response.text})

# Example function to get Jira issue comments
@csrf_exempt
def get_issue_comments(request):
    jira = connect_jira()
    issue_key = request.GET.get('issue_key')
    if not issue_key:
        return HttpResponseBadRequest('Issue key is required.')
    comments = jira.comments(issue_key)
    comment_list = [{'author': comment.author.displayName, 'body': comment.body} for comment in comments]
    return JsonResponse({'comments': comment_list})

# Example function to get Jira issue status
@csrf_exempt
def get_issue_status(request):
    jira = connect_jira()
    issue_key = request.GET.get('issue_key')
    if not issue_key:
        return HttpResponseBadRequest('Issue key is required.')
    issue = jira.issue(issue_key)
    return JsonResponse({'status': issue.fields.status.name})

@csrf_exempt
def process_llm_prompt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt")
        
        if not prompt:
            return JsonResponse({"error": "Prompt not provided"}, status=400)
        
        response = handle_prompt(prompt)
        
        if response["action"] == "error":
            return JsonResponse(response, status=400)
        
        if response["action"] == "create_issue":
            summary = response["issue"].get("summary")
            description = response["issue"].get("description")
            key = response["issue"].get("key")
            
            return JsonResponse({"message": "Issue created successfully", "issue": {
                "key": key,
                "summary": summary,
                "description": description
            }})
        
        if response["action"] == "view_issues":
            issues = view_issues()
            return JsonResponse({"message": "Issues found", "issues": issues})
        
        # TODO: implement these actions
        # if response["action"] == "get_issue_comments":
        #     issue_key = response["parameters"].get("issue_key")
        #     if not issue_key:
        #         return JsonResponse({"error": "Issue key not provided"}, status=400)
        #     comments = get_issue_comments(issue_key)
        #     return JsonResponse({"message": "Comments retrieved", "comments": comments})
        
        # if response["action"] == "add_comment":
        #     issue_key = response["parameters"].get("issue_key")
        #     comment = response["parameters"].get("comment")
        #     if not issue_key or not comment:
        #         return JsonResponse({"error": "Issue key or comment not provided"}, status=400)
        #     comment_result = add_comment(issue_key, comment)
        #     return JsonResponse({"message": comment_result["message"]})

        # if response["action"] == "edit_comment":
        #     issue_key = response["parameters"].get("issue_key")
        #     comment = response["parameters"].get("comment")
        #     if not issue_key or not comment:
        #         return JsonResponse({"error": "Issue key or comment not provided"}, status=400)
        #     edit_result = edit_comment(issue_key, comment)
        #     return JsonResponse({"message": edit_result["message"]})

        # if response["action"] == "get_issue_status":
        #     issue_key = response["parameters"].get("issue_key")
        #     if not issue_key:
        #         return JsonResponse({"error": "Issue key not provided"}, status=400)
        #     status = get_issue_status(issue_key)
        #     return JsonResponse({"message": "Issue status retrieved", "status": status})
        
        if response["action"] == "fetch_database":
            return JsonResponse({"message": "Notion database fetched", "data": response["data"]})
        
        if response["action"] == "fetch_page":
            return JsonResponse({"message": "Notion page fetched", "data": response["data"]})

        # Handle other actions here
        
        return JsonResponse({"error": "Unknown action"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)