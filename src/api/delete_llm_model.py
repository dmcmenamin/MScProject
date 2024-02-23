from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from src.models.llm_models import LlmModels


class DeleteLlmModel(Resource):
    """
    The delete method for the large language model and model
    :return: The response and status code
    """
    @classmethod
    @jwt_required()
    def delete(cls, llm_model_id):
        """
        The delete method for the large language model and model
        :return: The response and status code
        """
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            return {'message': 'You must be logged in to proceed'}, 401
        else:
            try:
                # check if the model exists
                llm_model_id = LlmModels.get_llm_model_by_id(llm_model_id)
                if not llm_model_id:
                    return {'message': 'Model does not exist'}, 404
                else:
                    # delete the large language model and model
                    LlmModels.delete_llm_by_id(llm_model_id)
                    return {'message': 'Model deleted successfully'}, 200
            except Exception as e:
                print(e)
                return {'message': 'Large language model and model could not be deleted'}, 500
