from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app import app
from src.models.api_key import ApiKey
from src.models.llm_name import Llm


# Class AddOrUpdateApiKey
# This class allows the user to add or update an api key
# - post: Adds or updates an api key

class AddOrUpdateApiKey(Resource):
    """
    The post method for adding or updating an api key
    :return: The response and status code
    """
    @classmethod
    @jwt_required()
    def post(cls):
        """
        The post method for adding or updating an api key
        :return: The response and status code
        """
        app.logger.info("Adding or updating api key")
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            app.logger.info("User not logged in")
            return {"message": "You must be logged in to proceed"}, 401
        else:
            try:
                # get the user input
                data = request.get_json()
                llm_name = data.get("llm_name")
                api_key = data.get("api_key")

                app.logger.info("User input: llm_name: %s, api_key: %s", llm_name, api_key)

                if not llm_name or not api_key:
                    return {"message": "Both llm_name and api_key are required"}, 400

                # check if the large language model exists
                llm = Llm.get_llm_by_name(llm_name)
                if llm is None:
                    app.logger.info("Large language model does not exist")
                    return {"message": "Large language model does not exist"}, 404
                else:
                    llm_id = llm.llm_id

                # user can only have 1 api key per large language model
                # check if the user already has an api key
                user_has_api_key = ApiKey.get_api_key_by_user_id_and_llm_id(logged_in_user_id, llm_id)
                app.logger.info("User has api key: %s", user_has_api_key)
                if user_has_api_key:
                    # update the api key
                    app.logger.info("Updating api key")
                    ApiKey.update_api_key_by_user_id_and_llm_id(logged_in_user_id, llm_name, api_key)
                    return {"message": "API Key updated successfully"}, 200
                else:
                    # add the api key
                    app.logger.info("Adding api key")
                    ApiKey.add_api_key(logged_in_user_id, llm_name, api_key)
                    return {"message": "API Key added successfully"}, 200
            except Exception as e:
                app.logger.error("API Key could not be added or updated" + str(e))
                return {"message": "API Key could not be added or updated"}, 500
