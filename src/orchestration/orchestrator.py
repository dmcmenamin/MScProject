
# class Orchestrator
#   The purpose of this class is to allow obfuscation of the Large Language Model being used
#   instead allowing for a single point of entry, so that different models can be used without
#   the user knowing.

class Orchestrator:
    """ Orchestrator class to handle all Large Language Model API calls
    """
    def __init__(self, large_language_model, api_key, model):
        """ Constructor for Orchestrator class
        :param large_language_model: The Large Language Model to use
        :param api_key: The API key
        :param model: The model
        """

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
        """ Returns the Large Language Model to be used
        :return: The Large Language Model to be used
        """

        if self.large_language_model == "ChatGPT":
            return self._call_chatgpt_api(self.api_key, self.model)
        elif self.large_language_model == "Bard":
            return self._call_bard_api()
        else:
            raise ValueError("Large Language Model is not supported.")

    def _call_chatgpt_api(self, api_key, model):
        """ Returns the ChatGPTAPI to be used
        :param api_key: The API key
        :param model: The model
        :return: The ChatGPTAPI to be used
        """
        from src.large_language_model.chatGPTAPI import ChatGPTAPI

        chatgpt = ChatGPTAPI(api_key, model)
        return chatgpt

    def _call_bard_api(self):
        """ Returns the BardAPI to be used - not implemented yet
        :return: The BardAPI to be used
        """
        pass
