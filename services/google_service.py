import json
import utils.constants as constants
import google.generativeai as genai
from services.base_service import BaseService

class GoogleService(BaseService):
    
    def __init__(self):
        super().__init__()
        self.model_name = constants.API['google']['model']
        genai.configure(api_key=constants.API['google']['key'])

    def get_response(self):
        model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self._system_prompt)
        response = model.generate_content(self._user_prompt)
        return self.response_parser(response)
    
    def response_parser(self, response):
        text = response.text.strip()
        if text.startswith("```json") and text.endswith("```"):
            json_str = text[len("```json"): -len("```")].strip()
            return json.loads(json_str)
        else:
            raise Exception("Response is not in expected JSON format")
        
