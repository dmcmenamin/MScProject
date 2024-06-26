from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app
from src.models.llm_models import LlmModels

# Class DeleteLlmModel
# This class allows the user to delete a large language model and model
# - delete: Deletes a large language model and model


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
        app.logger.info("Deleting large language model and model")
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            app.logger.info("User not logged in")
            return {"message": "You must be logged in to proceed"}, 401
        else:
            try:
                app.logger.info("User input: llm_model_id: %s", llm_model_id)
                # check if the model exists
                llm_model_id = LlmModels.get_llm_model_by_id(llm_model_id)
                if not llm_model_id:
                    app.logger.info("Model does not exist")
                    return {"message": "Model does not exist"}, 404
                else:
                    app.logger.info("Model exists")
                    # delete the large language model and model
                    LlmModels.delete_llm_by_id(llm_model_id)
                    app.logger.info("Model deleted successfully")
                    return {"message": "Model deleted successfully"}, 200
            except Exception as e:
                app.logger.error("Large language model and model could not be deleted" + str(e))
                return {"message": "Large language model and model could not be deleted"}, 500
