from flask_restful import Resource

from app import app
from src.models.llm_name import Llm

# Class GetAvailableLlms
# This class allows the user to get the available LLMs
# - get: Gets the available LLMs


class GetAvailableLlms(Resource):
    """
    The get method for the available LLMs
    :return: The available LLMs and status code
    """
    @classmethod
    def get(cls):
        """ The get method for the available LLMs
        :return: The available LLMs
        """

        app.logger.info("Getting available LLMs")
        try:
            app.logger.info("Checking for available LLMs")
            available_llms = Llm.return_all()
            if available_llms:
                app.logger.info("Available LLMs")
                llms = [{"llm_name": llm.llm_name, "llm_link": llm.llm_api_link} for llm in available_llms]
                return {"message": "Available LLMs", "data": llms}, 200
            else:
                app.logger.info("No available LLMs")
                return {"message": "No available LLMs"}, 404
        except Exception as e:
            app.logger.error("An error occurred" + str(e))
            return {"message": "An error occurred, please check database is online"}, 500
