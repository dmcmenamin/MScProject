from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db, app
from src.models.llm_models import LlmModels
from src.models.llm_name import Llm


class AddModel(Resource):
    """
    Add new model to the database
    :return: The response and status code
    """

    @classmethod
    @jwt_required()
    def post(cls):
        """
        The post method for adding a new model to the database
        :return: The response and status code
        """
        app.logger.info('Adding model')
        user_id = get_jwt_identity()
        if not user_id:
            app.logger.info('User not logged in')
            return {'message': 'User not logged in'}, 401

        # get user input
        data = request.get_json()

        # get the LLM name and model name and description from the request
        llm_name = data.get('llm_name')
        model_name = data.get('model_name')
        model_description = data.get('model_description')

        app.logger.info('User input: llm_name: %s, model_name: %s, model_description: %s',
                        llm_name, model_name, model_description)

        # get the llm_id
        llm_id = db.session.query(Llm.llm_id).filter(Llm.llm_name == llm_name).first()

        if not llm_id:
            app.logger.info('Large language model does not exist')
            return {'message': 'Large language model does not exist'}, 404

        try:
            app.logger.info('Large language model exists')
            # add the model to the database
            cls.add_model(llm_id[0], model_name, model_description)
            app.logger.info('Model added successfully')
            # set up the response
            data = {"llm_name": llm_name, "model_name": model_name, "model_description": model_description}
            return {'message': 'Model added successfully', 'data': data}, 200
        except Exception as e:
            app.logger.error('Model could not be added' + str(e))
            return {'message': 'Model could not be added'}, 500

    @classmethod
    def add_model(cls, llm_id, model_name, model_description):
        """
        Add a model to the database using the model name and description
        :param llm_id:
        :param model_name:
        :param model_description:
        :return: None
        """
        model = LlmModels(llm_id, model_name, model_description)
        db.session.add(model)
        db.session.commit()
