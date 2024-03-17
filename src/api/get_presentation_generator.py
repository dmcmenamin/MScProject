from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import select

from app import db
from src.models.api_key import ApiKey
from src.models.llm_models import LlmModels
from src.models.llm_name import Llm
from src.models.user_information import User
from src.utils.common_scripts import get_themes_available


class PresentationGeneratorGet(Resource):

    @jwt_required()
    def get(self):
        """ The get method for the presentation generator
        :return: The presentation generator page
        """

        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User not logged in'}, 401
        else:
            # get user's available llm model names
            api_keys_subquery = (db.session.query(ApiKey.api_key_llm)
                                 .join(User, User.user_id == ApiKey.api_key_user)
                                 .filter(User.user_id == user_id)
                                 .subquery())

            # filter the subquery to get distinct values using select and .c column command
            api_keys_select = select(api_keys_subquery.c.api_key_llm)

            # Now, query the LLMName table using the subquery above
            llm_model_names = (db.session.query(Llm.llm_name)
                               .filter(Llm.llm_id.in_(api_keys_select))
                               .all())

            llm_names_and_models = {}
            for llm_model_tuple in llm_model_names:
                llm_model = llm_model_tuple[0]  # Extract the string from the tuple
                llm_id = db.session.query(Llm.llm_id).filter(Llm.llm_name == llm_model).first()

                llm_details_and_description = db.session.query(LlmModels.llm_model_name,
                                                               LlmModels.llm_model_description) \
                    .filter(LlmModels.llm_id == llm_id[0]) \
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
            except Exception:
                return {'message': 'Something went wrong'}, 500
