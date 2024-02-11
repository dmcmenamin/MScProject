from flask import jsonify, logging, session

from src.controllers import common_scripts
from src.database import queries, database_scripts
from src.database.connection import RelDBConnection


def historical_endpoint_get():
    """ The historical endpoint for the API
    :return: The response and status code
    """

    database_connection = RelDBConnection()

    # Check if there is a connection to the database, if there is, check if the user exists
    try:
        # check if user exists
        params = (session['username'],)
        returned_historical_presentations = (database_connection.
                                             query_return_all_matches_with_parameter
                                             (queries.get_users_historical_presentations(), params))

        # if presentations exist
        if returned_historical_presentations:
            # return the historical presentations
            response_value = {"historical_data": returned_historical_presentations}
            return jsonify(response_value), 200
        elif len(returned_historical_presentations) == 0:
            # No historical information exists
            response_value = {"no_historical_data": "No historical data exists."}
            return jsonify(response_value), 200
        else:
            response_value = {"error": "Error Occurred."}
            return jsonify(response_value), 401
    except ConnectionError as e:
        response_value = {"error": "Connection to the database failed."}
        return jsonify(response_value), 500
    finally:
        # close the connection, just in case it is still open
        database_connection.close_connection()


def historical_endpoint_get_specific_presentation(presentation_id):
    """ Get a historically stored presentation
    :return: The response and status code
    """
    database_connection = RelDBConnection()

    # Check if there is a connection to the database, if there is, check if the user exists
    try:
        params = (presentation_id,)
        returned_historical_presentation = (database_connection.
                                            query_return_all_matches_with_parameter
                                            (queries.get_specific_historical_presentation(), params))

        # if presentation exists
        if returned_historical_presentation:
            # return the historical presentation
            response_value, status_code = common_scripts.download_presentation(returned_historical_presentation[0][1])
            return response_value, status_code
        elif len(returned_historical_presentation) == 0:
            # No historical information exists
            response_value = {"no_historical_presentation": "No historical presentation exists."}
            return jsonify(response_value), 401
        else:
            response_value = {"error": "Error Occurred."}
            return jsonify(response_value), 401
    except ConnectionError as e:
        response_value = {"error": "Connection to the database failed."}
        return jsonify(response_value), 500
    finally:
        # close the connection, just in case it is still open
        database_connection.close_connection()


def historical_endpoint_delete_specific_presentation(presentation_id):
    """ Delete a historically stored presentation
    :return: The response and status code
    """
    database_connection = RelDBConnection()

    # Check if there is a connection to the database, if there is, delete the presentation
    try:
        params = (presentation_id,)
        # if the presentation is deleted, return a success message
        database_connection.commit_query_with_parameter(queries.delete_specific_historical_presentation(), params)
        response_value = {"message": "Presentation deleted successfully"}
        return jsonify(response_value), 200
    except ConnectionError as e:
        response_value = {"error": "Connection to the database failed."}
        return jsonify(response_value), 500
    finally:
        # close the connection, just in case it is still open
        database_connection.close_connection()
