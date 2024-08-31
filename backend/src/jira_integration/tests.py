from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .llm_utils import handle_prompt, view_issues, create_jira_issue

class JiraIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('jira_integration.llm_utils.model.generate_content')
    def test_handle_prompt_view_issues(self, mock_generate_content):
        mock_generate_content.return_value.text = '{"action": "view_issues"}'
        
        with patch('jira_integration.llm_utils.view_issues') as mock_view_issues:
            mock_view_issues.return_value = {'action': 'view_issues', 'issues': []}
            result = handle_prompt("Show me all issues")
        
        self.assertEqual(result['action'], 'view_issues')

    @patch('jira_integration.llm_utils.model.generate_content')
    def test_handle_prompt_create_issue(self, mock_generate_content):
        mock_generate_content.return_value.text = '{"action": "create_issue", "summary": "Test Issue", "description": "Test Description"}'
        
        with patch('jira_integration.llm_utils.create_jira_issue') as mock_create_issue:
            mock_create_issue.return_value = {'action': 'create_issue', 'key': 'TEST-1', 'summary': 'Test Issue', 'description': 'Test Description'}
            result = handle_prompt("Create a new issue")
        
        self.assertEqual(result['action'], 'create_issue')
        self.assertEqual(result['key'], 'TEST-1')

    @patch('jira_integration.llm_utils.connect_jira')
    def test_view_issues(self, mock_connect_jira):
        mock_jira = MagicMock()
        mock_jira.search_issues.return_value = [
            MagicMock(key='TEST-1', fields=MagicMock(summary='Test Issue', description='Test Description', status=MagicMock(name='Open')))
        ]
        mock_connect_jira.return_value = mock_jira

        result = view_issues()
        
        self.assertEqual(result['action'], 'view_issues')
        self.assertEqual(len(result['issues']), 1)
        self.assertEqual(result['issues'][0]['key'], 'TEST-1')

    @patch('jira_integration.llm_utils.connect_jira')
    def test_create_jira_issue(self, mock_connect_jira):
        mock_jira = MagicMock()
        mock_new_issue = MagicMock(key='TEST-2', fields=MagicMock(summary='New Issue', description='New Description'))
        mock_jira.create_issue.return_value = mock_new_issue
        mock_connect_jira.return_value = mock_jira

        result = create_jira_issue('New Issue', 'New Description')
        
        self.assertEqual(result['action'], 'create_issue')
        self.assertEqual(result['key'], 'TEST-2')
        self.assertEqual(result['summary'], 'New Issue')

    def test_process_llm_prompt_view(self):
        with patch('jira_integration.views.handle_prompt') as mock_handle_prompt:
            mock_handle_prompt.return_value = {'action': 'chat', 'message': 'Test response'}
            response = self.client.post(reverse('process_llm_prompt'), {'prompt': 'Test prompt'}, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'action': 'chat', 'message': 'Test response'})

    def test_chat_interface_view(self):
        response = self.client.get(reverse('chat_interface'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jira_integration/chat_interface.html')