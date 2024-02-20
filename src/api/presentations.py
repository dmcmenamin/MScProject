from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from src.models.llm_name import Llm
from src.utils.common_scripts import get_themes_available


class PresentationGeneratorGet(Resource):

    @jwt_required()
    def get(self):
        """ The get method for the presentation generator
        :return: The presentation generator page
        """
        print("PresentationGeneratorGet")
        user_id = get_jwt_identity()
        if not user_id:
            print("User not logged in")
            return {'message': 'User not logged in'}, 401
        else:
            print("User logged in")
            llm_model_names = Llm.get_llm_model_names_by_user_id(user_id)
            llm_names_and_models = {}
            for llm_model in llm_model_names:
                llm_names_and_models[llm_model] = Llm.get_text_llm_model_information(llm_model)
            presentation_themes = get_themes_available()
            return {"llm_model_names": llm_model_names,
                    "llm_names_and_models": llm_names_and_models,
                    "presentation_themes": presentation_themes}, 200





        # # get user's available llm model names
        # database_connection = RelDBConnection()
        # params = (session['username'],)
        # returned_llm_model_names = (
        #     database_connection.
        #     query_return_all_matches_with_parameter(queries.get_all_llms_which_user_has_access_to(), params))
        # # convert list of tuples to list of strings
        # for i in range(len(returned_llm_model_names)):
        #     returned_llm_model_names[i] = returned_llm_model_names[i][0]
        #
        # # get specific llm models
        # llm_names_and_models = {}
        # for llm_model in returned_llm_model_names:
        #     llm_names_and_models[llm_model] = []
        #     params = (llm_model,)
        #     returned_llm_model_information = (
        #         database_connection.
        #         query_return_all_matches_with_parameter(queries.get_specific_llm(), params))
        #
        #     text_llm_model_information = []
        #     # convert list of tuples to list of strings for each llm model
        #     for i in range(len(returned_llm_model_information)):
        #         if returned_llm_model_information[i][3] == "text":
        #             # create a list of tuples containing the model name and description
        #             text_model_name_and_description = (returned_llm_model_information[i][2],
        #                                                returned_llm_model_information[i][4])
        #             text_llm_model_information.append(text_model_name_and_description)
        #     llm_names_and_models[llm_model] = text_llm_model_information
        #
        # #  get the themes available
        # presentation_themes = get_themes_available()
        #
        # # render presentation generator page with list of available llm model names
        # return jsonify({"llm_model_names": returned_llm_model_names,
        #                 "llm_names_and_models": llm_names_and_models,
        #                 "presentation_themes": presentation_themes}), 200