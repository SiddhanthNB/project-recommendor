import json
import requests
import utils.constants as constants
from services.base_service import BaseService

class OpenAIService(BaseService):

    def __init__(self):
        super().__init__()
        self._api_key = constants.API["openai"]["key"]
        self._url = constants.API["openai"]["url"]
        self.model_name = constants.API["openai"]["model"]

    def get_response(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": self._user_prompt}
            ]
        }
        response = requests.post(self._url, headers=headers, json=payload)
        response.raise_for_status()
        response = response.json()
        return self.response_parser(response["choices"][0]["message"]["content"])
    
    def response_parser(self, response):
        text = response.strip()
        start_marker = "```json"
        end_marker = "```"

        if start_marker not in text:
            raise Exception("No JSON block found in response")
        
        if end_marker not in text:
            raise Exception("No JSON block found in response")

        start_idx = text.index(start_marker) + len(start_marker)
        end_idx = text.index(end_marker, start_idx)
        json_str = text[start_idx:end_idx].strip()

        return json.loads(json_str)
