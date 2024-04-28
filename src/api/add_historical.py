from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app, db
from src.models.historical import Historical

# Class AddHistoricalPresentation
# This class allows the user to add a historical presentation to the database
# - post: Adds a historical presentation to the database

class AddHistoricalPresentation(Resource):

    @jwt_required()
    def post(self):

        app.logger.info("Adding historical presentation")
        user_id = get_jwt_identity()
        if not user_id:
            app.logger.info("User not logged in")
            return {"message": "User not logged in"}, 401
        else:
            try:
                app.logger.info("User logged in")

                # get user input
                app.logger.info("Data: %s", request.get_json())
                data = request.get_json()
                historical_user_id = user_id
                historical_presentation_name = data.get("presentation_name")
                historical_presentation_location = data.get("presentation_location")

                app.logger.info("User input: historical_user_id: %s, historical_presentation_name: %s, "
                                "historical_presentation_location: %s",
                                historical_user_id, historical_presentation_name, historical_presentation_location)

                # add the historical presentation to the database
                historical = Historical(historical_user_id=historical_user_id,
                                        historical_presentation_name=historical_presentation_name,
                                        historical_presentation_location=historical_presentation_location)
                db.session.add(historical)
                db.session.commit()

                app.logger.info("Historical presentation added successfully")
                # return the response
                data = {"historical_user_id": historical_user_id,
                        "historical_presentation_name": historical_presentation_name,
                        "historical_presentation_location": historical_presentation_location,
                        "historical_presentation_id": historical.historical_id}
                return {"message": "Historical presentation added successfully", "data": data}, 200
            except Exception as e:
                app.logger.error("Historical presentation could not be added" + str(e))
                return {"message": "Historical presentation could not be added"}, 500
