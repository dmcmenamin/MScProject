# Super class for Large Language Model
# it sets up the model which will be used by the child classes
# it also has the method to call the model which will be used by the child classes
# however it will not be instantiated as it is an abstract class

class LargeLanguageModel:
    """ LargeLanguageModel class to handle all Large Language Model API calls
    """
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def get_chat_response(self, question, llm_model):
        """ Returns a chat response from Large Language Model - should be implemented by child classes
        :param question: The question to ask Large Language Model
        :param llm_model: The Large Language Model to use
        :return: The chat response from Large Language Model
        """

        raise NotImplementedError("Subclass must implement abstract method")

    def set_question_prompt(self, presenter_name, presentation_topic, audience_size, presentation_length,
                            audience_outcome):
        """ Returns a question prompt for Large Language Model - should be implemented by child classes
        :param presenter_name: The name of the presenter
        :param presentation_topic: The topic of the presentation
        :param audience_size: The audience size of the presentation
        :param presentation_length: The time of the presentation
        :param audience_outcome: A description of what you expect the audience to
                                 know or be able to do after the presentation
        :return: The question prompt for Large Language Model
        """

        raise NotImplementedError("Subclass must implement abstract method")

    def get_presentation_slides(self, question):
        """ Returns a presentation deck from Large Language Model - should be implemented by child classes
        :param question: The question to ask Large Language Model
        :return: The presentation deck from Large Language Model
        """

        raise NotImplementedError("Subclass must implement abstract method")

    def get_presentation_image(self, image_query, image_size):
        """ Returns an image from Large Language Model - should be implemented by child classes
        :param image_query: The image query to ask Large Language Model
        :param image_size: The image size to ask Large Language Model
        :return: The image from Large Language Model
        """

        raise NotImplementedError("Subclass must implement abstract method")



