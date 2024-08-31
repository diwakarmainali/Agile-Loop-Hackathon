# agile-loop-hackathon - Backend Development - Jira Issue Management with LLM Integration

# Project Summary: Jira Issue Management with LLM Integration

# How to run project
## Requirements
- Python 3
- access to
--- JIRA
--- Gemini

## Setting up environment

Use virtual env to create an python development environment

Create virtual env (venv) by running this command

`python -m venv venv`

and enable the virtual env by running this command

`source venv/bin/activate`

once you have enabled the virtual environment, install the modules defined in requirements.txt by running

`pip install -r requirements.txt`

### Setting up environment - Credentials

Once you have installed all of the dependencies and setting up the virtual environment, you need to set up the project credentials through .env file

follows template on `.env.copy` and fill with your project credentials and then create a new file with name `.env`

## Running project

to run the Django server by going to `/src` folder and run

`python manage.py runserver` --> by default will run on port :8000

before running for the first time, please do migration by running this command

`python manage.py migrate`

## Available interface
| Feature       | Endpoint                 | Payload                                     |
|---------------|--------------------------|---------------------------------------------|
| LLM prompt    | POST /process-llm-prompt | JSON `{ "prompt": "<MESSAGE PROMPT HERE>" }`|

## Current State
1. Basic Jira integration is implemented (view issues).
2. Django backend with endpoints for Jira operations.
3. Initial LLM integration using Google's Gemini model.

## Next Steps

1. Enhance LLM Integration:
   - Refine the prompt handling in `handle_prompt` function.
   - Implement more robust extraction of issue details from LLM responses.

2. Extend API Functionality:
   - Add more Jira operations (e.g., update issues, add comments).
   - Implement error handling and input validation.

3. Improve LLM-to-API Mapping:
   - Develop a more sophisticated system to map LLM responses to API calls.
   - Consider using a structured output format from Gemini (JSON responses).

4. Frontend Development:
   - Create or enhance the chat interface for user interactions.
   - Implement real-time updates and feedback.

5. Testing and Refinement:
   - Develop unit tests for LLM integration and Jira operations.
   - Perform user testing and gather feedback.

6. Security and Performance:
   - Implement proper authentication and authorization.
   - Optimize API calls and LLM interactions for better performance.

7. Documentation:
   - Create comprehensive documentation for the system.
   - Provide usage guidelines and examples.

## Integration Workflow

1. User sends prompt to LLM: "I want to view all open issues"
2. LLM receives prompt and analyzes user request
3. LLM identifies the intent (e.g., "view open issues")
4. Backend maps the intent to the appropriate API call (e.g., `view_issues()`)
5. API call is executed, and results are returned
6. Results are formatted and sent back to the user

## Technical Considerations

- Use Gemini 1.5 Flash or Pro model for JSON output capabilities.
- Implement structured output using `response_mime_type` and `response_schema`.
- Consider using typed dictionaries for structured responses.
- Enhance error handling and logging throughout the application.


# LLM Assistance (This is response from an LLM on how to move forward) 

Thank you for providing the context and code snippets. It seems you're working on integrating an LLM (specifically Google's Gemini model) into your Jira issue management system. Let's break down the next steps and how to integrate it based on what you've discussed:
Project Summary and Next StepsClick to open document
Based on your current implementation and plans, here are my suggestions for the next steps:

### Enhance LLM Integration:

Refine the handle_prompt function in llm_utils.py to better parse and understand user intents.
Implement more sophisticated regex patterns or consider using a more advanced NLP technique to extract actions and parameters from LLM responses.


### Structured LLM Responses:

Utilize Gemini's JSON output capability by setting response_mime_type to "application/json" and defining a response_schema.
This will make it easier to extract specific information from LLM responses.


### Extend API Functionality:

Add more Jira operations to your llm_utils.py file, such as updating issues, adding comments, or changing issue status.
Ensure proper error handling and validation for all API calls.


### Improve LLM-to-API Mapping:

Create a more robust system to map LLM intents to specific API calls.
Consider creating a mapping dictionary or using a more advanced routing system.


### Frontend Development:

Enhance the chat interface (chat_interface.html) to provide a smoother user experience.
Implement real-time updates using JavaScript to fetch and display results asynchronously.


### Testing and Refinement:

Develop unit tests for your LLM integration and Jira operations.
Perform user testing to gather feedback on the natural language interface.



Here's an example of how you might modify the handle_prompt function to use structured JSON output from Gemini:
Enhanced handle_prompt functionClick to open code
This enhanced handle_prompt function uses Gemini's JSON output capability to get a structured response, making it easier to determine the appropriate action and extract any necessary parameters.
To implement this, you'll need to:

Update your llm_utils.py file with this new function.
Modify your views.py file to use this new function in the process_llm_prompt view.
Ensure your frontend can handle the structured responses.

Remember to handle potential errors, such as invalid JSON responses or unexpected action types.
Would you like me to elaborate on any of these steps or provide more specific code examples for other parts of the integration? CopyRetryLFhow is thsi work flow working like? help me understand and use an example EditCertainly! Let's walk through the workflow of this enhanced system using an example. I'll explain each step of the process to help you understand how it all comes together.
LLM-Jira Integration WorkflowClick to open diagram
Now, let's go through an example of this workflow step by step:

User Input:
The user types into the chat interface: "I need to create a new issue for a bug in the login system"
Frontend to Backend:
The frontend JavaScript sends this prompt to the backend, specifically to the process_llm_prompt view in views.py.
Backend to LLM:
The process_llm_prompt view calls the handle_prompt function in llm_utils.py. This function then sends the prompt to the Gemini LLM for analysis.
LLM Processing:
The LLM analyzes the prompt and determines that the user wants to create a new issue. It generates a structured JSON response like this:
jsonCopy{
  "action": "create_issue",
  "parameters": {
    "summary": "Bug in login system",
    "description": "A new issue has been reported regarding a bug in the login system. Further investigation is needed to determine the specific nature of the bug."
  }
}

Backend Processing:
The handle_prompt function receives this JSON response and interprets it. Since the action is "create_issue", it calls the create_jira_issue function with the provided summary and description.
Jira API Interaction:
The create_jira_issue function connects to the Jira API and creates a new issue with the given details.
Result Handling:
The Jira API returns the details of the newly created issue. The backend formats this into a response, perhaps something like:
jsonCopy{
  "message": "Issue created successfully",
  "issue": {
    "key": "PROJ-123",
    "summary": "Bug in login system",
    "description": "A new issue has been reported regarding a bug in the login system. Further investigation is needed to determine the specific nature of the bug.",
    "status": "Open"
  }
}

Frontend Display:
This response is sent back to the frontend, which then updates the chat interface to show the user that their issue has been created, displaying the key and other relevant details.

This workflow allows for a natural language interaction where the user doesn't need to know the specifics of how to create a Jira issue. The LLM interprets their intent, and the backend system translates that into the appropriate API calls.
The same workflow would apply for other actions, like viewing issues. The LLM would recognize the intent (e.g., "show me all open bugs"), and the backend would translate that into the appropriate Jira API call to fetch and return the relevant issues.