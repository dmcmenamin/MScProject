from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db
from src.models.llm_models import LlmModels
from src.models.llm_name import Llm


class AddLlmAndModel(Resource):
    """
    Add new large language model and model to the database
    :return: The response and status code
    """

    @classmethod
    @jwt_required()
    def post(cls):
        """
        The post method for adding a new large language model and model to the database
        :return: The response and status code
        """
        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User not logged in'}, 401
        else:
            try:
                # get user input
                data = request.get_json()
                llm_name = data.get('llm_name')
                llm_api_link = data.get('llm_api_link')
                model_name = data.get('model_name')
                model_description = data.get('model_description')

                # add the large language model to the database
                llm = Llm(llm_name=llm_name, llm_api_link=llm_api_link)
                db.session.add(llm)
                db.session.commit()

                # add the model to the database
                llm_id = db.session.query(Llm.llm_id).filter(Llm.llm_name == llm_name).first()
                model = LlmModels(llm_id=llm_id[0], llm_model_name=model_name, llm_model_description=model_description)
                db.session.add(model)
                db.session.commit()

                # return the response
                data = {"llm_name": llm_name, "model_name": model_name, "model_description": model_description}
                return {'message': 'Large language model and model added successfully' , 'data': data}, 200
            except Exception as e:
                print(e)
                return {'message': 'Large language model and model could not be added'}, 500
