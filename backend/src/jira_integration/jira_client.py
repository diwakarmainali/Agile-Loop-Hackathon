
from jira import JIRA

class JiraClient:
    def __init__(self, server, username, token):
        self.jira = JIRA(server=server, basic_auth=(username, token))
    
    def create_ticket(self, project_key, summary, description, issue_type):
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        return self.jira.create_issue(fields=issue_dict)
    
    def add_task(self, issue_key, summary, description):
        subtask = {
            'project': {'key': issue_key.split('-')[0]},
            'parent': {'key': issue_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Sub-task'},
        }
        return self.jira.create_issue(fields=subtask)
    
    def get_completion_date(self, issue_key):
        issue = self.jira.issue(issue_key)
        return issue.fields.duedate
    
    def get_issue_data(self, issue_key):
        issue = self.jira.issue(issue_key)
        return {
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status.name,
            'completion_date': issue.fields.duedate,
        }
