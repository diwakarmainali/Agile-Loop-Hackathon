import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

NOTION_BASE_URL = "https://api.notion.com/v1"

DEFAULT_NOTION_HEADERS = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + os.getenv("NOTION_API_KEY")
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