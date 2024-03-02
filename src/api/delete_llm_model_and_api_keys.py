from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app
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
        app.logger.info('Deleting large language model and model and API Keys')

        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            app.logger.info('User not logged in')
            return {'message': 'You must be logged in to proceed'}, 401
        else:
            try:
                # check if the model exists
                app.logger.info('User input: llm_id: %s', llm_id)
                llm_name = Llm.get_llm_by_id(llm_id)
                if not llm_name:
                    app.logger.info('Large language model does not exist')
                    return {'message': 'Large language model does not exist'}, 404
                else:
                    app.logger.info('Large language model exists')
                    # delete the large language model and model
                    LlmModels.delete_all_llm_models_by_llm_id(llm_id)
                    ApiKey.delete_api_key_by_llm_id(llm_id)
                    Llm.delete_llm_by_id(llm_id)
                    app.logger.info('Large language model, model and API Keys deleted successfully')
                    return {'message': 'Large language model, model and API Keys successfully deleted'}, 200
            except Exception as e:
                app.logger.error('Large language model and model could not be deleted' + str(e))
                return {'message': 'Large language model and model could not be deleted'}, 500
