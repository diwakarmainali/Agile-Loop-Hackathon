

import requests

class AIClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
    
    def generate_summary(self, text):
        response = requests.post(
            self.api_url,
            headers={'Authorization': f'Bearer {self.api_key}'},
            json={'text': text}
        )
        response.raise_for_status()
        return response.json()
