from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import select

from app import db
from src.database import queries
from src.database.connection import RelDBConnection
from src.models.api_key import ApiKey
from src.models.llm_details import LlmDetails
from src.models.llm_name import Llm
from src.models.user import User
from src.utils.common_scripts import get_themes_available


class PresentationGeneratorGet(Resource):

    @jwt_required()
    def get(self):
        """ The get method for the presentation generator
        :return: The presentation generator page
        """

        username = get_jwt_identity()
        if not username:
            return {'message': 'User not logged in'}, 401
        else:
            user_id_tuple = db.session.query(User.user_id).filter(User.username == username).first()
            user_id = user_id_tuple[0]
            # get user's available llm model names
            api_keys_subquery = (db.session.query(ApiKey.api_key_llm).join(User, User.user_id == ApiKey.api_key_user).
                                 filter(User.user_id == user_id).subquery())

            # Now, query the LLMName table using the subquery above
            llm_model_names = db.session.query(Llm.LLM_Name_Name).filter(Llm.LLM_Name_ID.in_(api_keys_subquery)).all()

            llm_names_and_models = {}
            llm_names_and_models = {}
            for llm_model_tuple in llm_model_names:
                llm_model = llm_model_tuple[0]  # Extract the string from the tuple
                llm_id = db.session.query(Llm.LLM_Name_ID).filter(Llm.LLM_Name_Name == llm_model).first()

                llm_details_and_description = db.session.query(LlmDetails.LLM_Model_Name,
                                                               LlmDetails.llm_details_description) \
                    .filter(LlmDetails.LLM_Name_ID == llm_id[0]) \
                    .all()

                # Convert each detail tuple to a dict
                details_list = [{'model_name': detail[0], 'description': detail[1]} for detail in
                                llm_details_and_description]

                llm_names_and_models[
                    llm_model] = details_list  # Use the string `llm_model` as the key instead of a tuple

            # get the themes available
            presentation_themes = get_themes_available()

            try:
                data = {"llm_model_names": [{"name": llm_model[0]} for llm_model in llm_model_names],
                        "llm_names_and_models": llm_names_and_models,
                        "presentation_themes": presentation_themes}
                return {'message': 'Success', 'data': data}, 200
            except Exception as e:
                return {'message': 'Something went wrong'}, 500
