from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app
from src.models.historical import Historical

# Class GetAllHistoricalForUser
# This class allows the user to get all historical data for a user
# - get: Gets all historical data for a user


class GetAllHistoricalForUser(Resource):

    @jwt_required()
    def get(self, user_id):
        """
        The get method for the historical data for the user id
        :param user_id: The user id to get the historical data for
        :return: The response and status code
        """
        user = get_jwt_identity()

        if user_id != str(user):
            app.logger.info("User not logged in")
            return {"message": "User not logged in"}, 401

        app.logger.info("Getting historical data for user")
        if not user_id:
            app.logger.info("User not logged in")
            return {"message": "User not logged in"}, 401
        else:
            try:
                app.logger.info("User input: user_id: %s", user_id)
                # get the historical data for the user
                historical_data = Historical.find_all_presentations_by_user_id(user_id)

                if not historical_data:
                    app.logger.info("No historical data found")
                    return {"message": "No historical data found"}, 404
                else:
                    app.logger.info("Historical data found")
                    data = {"historical_data": [{"historical_id": historical.historical_id,
                                                 "presentation_name": historical.historical_presentation_name,
                                                 "presentation_location": historical.historical_presentation_location,
                                                 "presentation_time_stamp": historical.convert_time_stamp_to_string(),
                                                 "user_id": historical.historical_user_id}
                                                for historical in historical_data]}
                    return {"message": "Historical data found", "data": data}, 200
            except Exception as e:
                app.logger.error("Historical data could not be found" + str(e))
                return {"message": "Historical data could not be found"}, 500
