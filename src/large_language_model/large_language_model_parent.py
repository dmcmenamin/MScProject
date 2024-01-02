# Super class for Large Language Model
# it sets up the model which will be used by the child classes
# it also has the method to call the model which will be used by the child classes
# however it will not be instantiated as it is an abstract class

class LargeLanguageModel:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def get_chat_response(self, question, llm_model):
        raise NotImplementedError("Subclass must implement abstract method")

    def set_question_prompt(self, topic, audience_size, time):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_presentation_slides(self, question):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_presentation_image(self, image_query, image_size):
        raise NotImplementedError("Subclass must implement abstract method")



