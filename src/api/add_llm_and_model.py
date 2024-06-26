from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db, app
from src.api.add_model import AddModel
from src.models.llm_name import Llm

# Class AddLlmAndModel
# This class allows the user to add a new large language model and model to the database
# - post: Adds a new large language model and model to the database


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
        app.logger.info("Adding large language model and model")
        user_id = get_jwt_identity()
        if not user_id:
            app.logger.info("User not logged in")
            return {"message": "User not logged in"}, 401
        else:
            try:
                # get user input
                data = request.get_json()
                llm_name = data.get("llm_name")
                llm_api_link = data.get("llm_api_link")
                model_name = data.get("model_name")
                model_description = data.get("model_description")

                app.logger.info("User input: llm_name: %s, llm_api_link: %s, model_name: %s, model_description: %s",
                                llm_name, llm_api_link, model_name, model_description)

                # add the large language model to the database
                llm = Llm(llm_name=llm_name, llm_api_link=llm_api_link)
                db.session.add(llm)
                db.session.commit()

                app.logger.info("Large language model added successfully")
                # add the model to the database
                llm_id = db.session.query(Llm.llm_id).filter(Llm.llm_name == llm_name).first()
                AddModel.add_model(llm_id[0], model_name, model_description)

                app.logger.info("Model added successfully")
                # return the response
                data = {"llm_name": llm_name, "model_name": model_name, "model_description": model_description}
                return {"message": "Large language model and model added successfully", "data": data}, 200
            except Exception as e:
                app.logger.error("Large language model and model could not be added" + str(e))
                return {"message": "Large language model and model could not be added"}, 500
