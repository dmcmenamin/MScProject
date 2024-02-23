from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from src.models.api_key import ApiKey
from src.models.llm_models import LlmModels
from src.models.llm_name import Llm


class DeleteLlmAndModelAndApiKeys(Resource):
    """
    The delete method for the large language model and model and api keys
    :return: The response and status code
    """
    @classmethod
    @jwt_required()
    def delete(cls, llm_id):
        """
        The delete method for the large language model and model and api keys
        :return: The response and status code
        """
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            return {'message': 'You must be logged in to proceed'}, 401
        else:
            try:
                # check if the model exists
                llm_name = Llm.get_llm_by_id(llm_id)
                if not llm_name:
                    return {'message': 'Large language model does not exist'}, 404
                else:
                    # delete the large language model and model
                    LlmModels.delete_all_llm_models_by_llm_id(llm_id)
                    ApiKey.delete_api_key_by_llm_id(llm_id)
                    Llm.delete_llm_by_id(llm_id)
                    return {'message': 'Large language model, model and API Keys successfully deleted'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Large language model and model could not be deleted'}, 500
