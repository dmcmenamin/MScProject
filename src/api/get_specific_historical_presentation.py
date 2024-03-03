from flask_restful import Resource

from app import app
from src.models.historical import Historical
from src.utils.common_scripts import download_presentation


class GetSpecificHistoricalPresentation(Resource):

    @classmethod
    def get(cls, historical_id):
        """
        The get method for the specific historical presentation
        :return: The response and status code
        """
        app.logger.info('Getting specific historical presentation')
        try:
            # get the presentation
            presentation = Historical.find_historical_by_historical_id(historical_id)
            app.logger.info('Presentation: %s', presentation)
            print(presentation.historical_presentation_location + "/" + presentation.historical_presentation_name + ".pptx")
            if presentation:
                # download the file from the presentation location
                response, status_code = download_presentation(presentation.historical_presentation_location + "/" +
                                                              presentation.historical_presentation_name + ".pptx")
                if status_code == 200:
                    app.logger.info('Presentation downloaded')
                    return {'message': 'Presentation downloaded'}, 200
                else:
                    app.logger.error('Error downloading presentation, check it exists in the location specified')
                    return {'message': 'Error downloading presentation'}, 500
            else:
                return {'message': 'Presentation not found'}, 404
        except Exception as e:
            app.logger.error('Error getting specific historical presentation' + str(e))
            return {'message': 'Error getting specific historical presentation'}, 500
