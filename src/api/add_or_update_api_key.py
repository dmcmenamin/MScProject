from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from src.models.api_key import ApiKey
from src.models.llm_name import Llm


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
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            return {'message': 'You must be logged in to proceed'}, 401
        else:
            try:
                # get the user input
                data = request.get_json()
                llm_name = data.get('llm_name')
                api_key = data.get('api_key')

                if not llm_name or not api_key:
                    return {'message': 'Both llm_name and api_key are required'}, 400

                print("llm_name: ", llm_name)
                # check if the large language model exists
                llm = Llm.get_llm_by_name(llm_name)
                if llm is None:
                    return {'message': 'Large language model does not exist'}, 404
                else:
                    llm_id = llm.llm_id
                print(logged_in_user_id, llm_id, llm_name, api_key)
                # user can only have 1 api key per large language model
                # check if the user already has an api key
                user_has_api_key = ApiKey.get_api_key_by_user_id_and_llm_id(logged_in_user_id, llm_id)
                if user_has_api_key:
                    # update the api key
                    ApiKey.update_api_key_by_user_id_and_llm_id(logged_in_user_id, llm_name, api_key)
                    return {'message': 'API Key updated successfully'}, 200
                else:
                    # add the api key
                    ApiKey.add_api_key(logged_in_user_id, llm_name, api_key)
                    return {'message': 'API Key added successfully'}, 200
            except Exception as e:
                print(e)
                return {'message': 'API Key could not be added or updated'}, 500
