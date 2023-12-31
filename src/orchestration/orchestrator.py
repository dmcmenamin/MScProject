from src.api.chatGPTAPI import ChatGPTAPI


# class Controller:
#   The purpose of this class is to allow obfuscation of the Large Language Model being used
#   instead allowing for a single point of entry, so that different models can be used without
#   the user knowing.

class Orchestrator:
    def __init__(self, large_language_model, api_key, model):

        if not large_language_model:
            raise ValueError("Large Language Model cannot be empty.")
        else:
            self.large_language_model = large_language_model
        if not api_key:
            raise ValueError("OpenAI API key cannot be empty.")
        else:
            self.api_key = api_key

        # exclude validation on model - as it is unknown at this point if Bard may use Model
        # it is being done at ChatGPTAPI api level for that model
        self.model = model

    def call_large_language_model(self):
        if self.large_language_model == "ChatGPT":
            return self.call_chatgpt_api(self.api_key, self.model)
        elif self.large_language_model == "Bard":
            return self.call_bard_api()
        else:
            raise ValueError("Large Language Model is not supported.")

    def call_chatgpt_api(self, api_key, model):
        chatgpt = ChatGPTAPI(api_key, model)
        return chatgpt

    def call_bard_api(self):
        pass
