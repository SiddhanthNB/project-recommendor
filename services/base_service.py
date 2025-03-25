class BaseService:

    def __init__(self):
        with open('utils/prompts/system_prompt.txt', 'r') as file:
            self._system_prompt = file.read().strip()

        with open('utils/prompts/user_prompt.txt', 'r') as file:
            self._user_prompt = file.read().strip()
