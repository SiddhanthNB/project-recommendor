import requests
import utils.constants as constants
from services.base_service import BaseService

class HuggingFaceService(BaseService):

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
        return response["choices"][0]["message"]
