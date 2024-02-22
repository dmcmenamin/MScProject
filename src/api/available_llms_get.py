from flask_restful import Resource

from src.models.llm_name import Llm


class AvailableLlmsGet(Resource):
    """
    The get method for the available LLMs
    :return: The available LLMs and status code
    """
    @classmethod
    def get(cls):
        """ The get method for the available LLMs
        :return: The available LLMs
        """
        available_llms = Llm.return_all()

        if available_llms:
            llms = [{"llm_name": llm.LLM_Name_Name} for llm in available_llms]
            return {"message": "Available LLMs", "data": llms}, 200
        else:
            return {"message": "No available LLMs"}, 404
