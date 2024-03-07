import os

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app
from src.models.historical import Historical
from src.utils.common_scripts import delete_file_of_type_specified


class DeleteHistoricalPresentation(Resource):

    @jwt_required()
    def delete(self, historical_id):

        app.logger.info('Deleting historical presentation')
        user_id = get_jwt_identity()

        if not user_id:
            app.logger.info('User not logged in')
            return {'message': 'You must be logged in to proceed'}, 401
        else:
            try:
                app.logger.info('User input: historical_id: %s', historical_id)
                # delete the historical presentation
                historical_presentation_location = Historical.find_historical_location_by_historical_id(historical_id)
                if historical_presentation_location:
                    # delete the user's presentations
                    app.logger.info('Historical presentation locations: %s', historical_presentation_location)
                    # delete the files
                    if os.path.exists(historical_presentation_location):
                        delete_file_of_type_specified(historical_presentation_location)
                        app.logger.info('Historical presentation deleted successfully')
                    else:
                        app.logger.info('Historical presentation not found')

                    # delete the historical presentation from the database
                    Historical.delete_historical_by_historical_id(historical_id)
                    app.logger.info('Historical presentation deleted successfully')
                    return {'message': 'Historical presentation deleted successfully'}, 200
                else:
                    app.logger.info('Historical presentation not found')
                    return {'message': 'Historical presentation not found'}, 404
            except Exception as e:
                app.logger.error('Error deleting historical presentation' + str(e))
                return {'message': 'Error deleting historical presentation'}, 500
