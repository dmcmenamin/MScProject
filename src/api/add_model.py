from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db
from src.models.llm_models import LlmModels
from src.models.llm_name import Llm


class AddModel(Resource):
    """
    Add new model to the database
    :return: The response and status code
    """

    @classmethod
    @jwt_required()
    def post(self):
        """
        The post method for adding a new model to the database
        :return: The response and status code
        """

        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User not logged in'}, 401

        # get user input
        data = request.get_json()

        # get the LLM name and model name and description from the request
        llm_name = data.get('llm_name')
        model_name = data.get('model_name')
        model_description = data.get('model_description')

        # get the llm_id
        llm_id = db.session.query(Llm.llm_id).filter(Llm.llm_name == llm_name).first()

        if not llm_id:
            return {'message': 'Large language model does not exist'}, 404

        try:
            # add the model to the database
            model = LlmModels(llm_id=llm_id[0], llm_model_name=model_name, llm_model_description=model_description)
            db.session.add(model)
            db.session.commit()

            # set up the response
            data = {"llm_name": llm_name, "model_name": model_name, "model_description": model_description}
            return {'message': 'Model added successfully', 'data': data}, 200
        except Exception as e:
            print(e)
            return {'message': 'Model could not be added'}, 500
