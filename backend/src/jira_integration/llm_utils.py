# jira_automation/jira_integration/llm_utils.py

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import sys
import json
import requests
from jira import JIRA
from dotenv import load_dotenv
from typing import List, Dict, Any

import sys
import os

# Append the parent directory to sys.path to allow for imports beyond the top-level package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can perform imports from the parent directory or other directories at the same level
from notion_integration import notion_lib

# Load environment variables
load_dotenv()

# Initialize the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

def connect_jira():
    jira_options = {'server': f"https://{os.getenv('JIRA_DOMAIN')}.atlassian.net"}
    jira = JIRA(options=jira_options, basic_auth=(os.getenv('EMAIL'), os.getenv('JIRA_API_KEY')))
    return jira

def view_issues() -> List[Dict[str, Any]]:
    jira = connect_jira()
    issues = jira.search_issues(f"project={os.getenv('JIRA_PROJECT_KEY')}")
    
    issues_list = []
    for issue in issues:
        issues_list.append({
            'key': issue.key,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status.name,
        })
    
    return issues_list

def create_issue(summary: str, description: str) -> Dict[str, Any]:
    jira = connect_jira()
    issue_dict = {
        'project': {'key': os.getenv('JIRA_PROJECT_KEY')},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    print(new_issue)
    print({
        'key': new_issue.key,
        'summary': summary,
        'description': description,
    })

    return {
        'key': new_issue.key,
        'summary': summary,
        'description': description,
    }

def get_all_users() -> List[Dict[str, str]]:
    jira = connect_jira()
    # TODO: query must be specified for this search users to work
    users = jira.search_users()
    return [{'name': user.displayName, 'email': user.emailAddress} for user in users]

def create_user(display_name: str, email: str, password: str) -> Dict[str, Any]:
    jira = connect_jira()
    new_user = jira.create_user(
        username=email,
        email=email,
        display_name=display_name,
        password=password
    )
    return {
        'name': new_user.displayName,
        'email': new_user.emailAddress,
    }

def add_file_attachment(issue_key: str, file_path: str) -> Dict[str, Any]:
    jira = connect_jira()
    issue = jira.issue(issue_key)
    attachment = jira.add_attachment(issue=issue, attachment=file_path)
    return {
        'filename': attachment.filename,
        'size': attachment.size,
    }

def get_issue_comments(issue_key: str) -> List[Dict[str, str]]:
    jira = connect_jira()
    comments = jira.comments(issue_key)
    return [{'author': comment.author.displayName, 'body': comment.body} for comment in comments]

def add_comment(issue_key: str, comment: str) -> Dict[str, str]:
    jira = connect_jira()
    new_comment = jira.add_comment(issue_key, comment)
    return {
        'author': new_comment.author.displayName,
        'body': new_comment.body,
    }

def edit_comment(issue_key: str, comment_id: str, new_comment: str) -> Dict[str, str]:
    jira = connect_jira()
    updated_comment = jira.comment(issue_key, comment_id).update(body=new_comment)
    return {
        'author': updated_comment.author.displayName,
        'body': updated_comment.body,
    }

def get_issue_status(issue_key: str) -> str:
    jira = connect_jira()
    issue = jira.issue(issue_key)
    return issue.fields.status.name

def handle_prompt(prompt: str) -> Dict[str, Any]:
    try:
        response = model.generate_content(
            f"""
            Analyze the following user prompt and determine the which service and action that user want to use:
            
            {prompt}
            
            Respond with a JSON object containing the service, action and any relevant parameters.
            
            Valid services are:
            - "JIRA"
            - "NOTION"

            Valid actions are:
            - "view_issues"
            - "create_issue"
            - "get_all_users"
            - "create_user"
            - "add_file_attachment"
            - "get_issue_comments"
            - "add_comment"
            - "edit_comment"
            - "get_issue_status"
            - "fetch_database"
            - "fetch_page"
            
            Include relevant parameters for each action.
            """,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        )

        prompt_response = json.loads(response.text)
        prompt_message_for_service = ""
        service = prompt_response.get('service')

        print(f"service: {service}")

        if service != 'JIRA' and service != 'NOTION':
            return {'action': 'error', 'message': 'Your intented service is not supported'}

        action = prompt_response.get('action')
        parameters = prompt_response.get('parameters', {})
        
        # Print the action and parameters
        print(f"Action: {action}, Parameters: {parameters}")

        if action == 'view_issues':
            return {'action': action, 'issues': view_issues()}
        elif action == 'create_issue':
            return {'action': action, 'issue': create_issue(parameters.get('summary'), parameters.get('description'))}
        # TODO: implement these actions
        # elif action == 'get_all_users':
        #     return {'action': action, 'users': get_all_users()}
        # elif action == 'create_user':
        #     return {'action': action, 'user': create_user(parameters.get('display_name'), parameters.get('email'), parameters.get('password'))}
        # elif action == 'add_file_attachment':
        #     return {'action': action, 'attachment': add_file_attachment(parameters.get('issue_key'), parameters.get('file_path'))}
        # elif action == 'get_issue_comments':
        #     return {'action': action, 'comments': get_issue_comments(parameters.get('issue_key'))}
        # elif action == 'add_comment':
        #     return {'action': action, 'comment': add_comment(parameters.get('issue_key'), parameters.get('comment'))}
        # elif action == 'edit_comment':
        #     return {'action': action, 'comment': edit_comment(parameters.get('issue_key'), parameters.get('comment_id'), parameters.get('new_comment'))}
        # elif action == 'get_issue_status':
        #     return {'action': action, 'status': get_issue_status(parameters.get('issue_key'))}
        elif action == 'fetch_database':
            return {'action': action, 'data': notion_lib.fetch_databases(parameters.get('database_id'))}
        elif action == 'fetch_page':
            return {'action': action, 'data': notion_lib.fetch_pages(parameters.get('page_id'))}
        else:
            return {'action': 'error', 'message': 'Invalid action'}
    
    except google_exceptions.InvalidArgument as e:
        return {"action": "error", "message": str(e)}
    except Exception as e:
        return {"action": "error", "message": f"An unexpected error occurred: {str(e)}"}