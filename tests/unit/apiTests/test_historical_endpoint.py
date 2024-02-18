import unittest
from flask import session
import app  # Import a function to create your Flask app
from src.database.connection import RelDBConnection
from unittest.mock import patch, MagicMock


# Mocking database responses and session
def mock_query_return_all_matches_with_parameter(*args, **kwargs):
    # Mock based on the input args, kwargs or just return a general mock
    if "specific_historical_presentation" in args[0]:
        return [("presentation_id", "/path/to/presentation.pptx")]
    return []


def mock_query_return_no_matches(*args, **kwargs):
    return []


def mock_commit_query_with_parameter(*args, **kwargs):
    pass


def mock_delete_file_of_type_specified(file_location, file_type):
    pass


class HistoricalEndpointTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test application client"""
        self.app = app()
        self.client = self.app.test_client()

        # You could also mock session here if needed
        # with self.app.test_request_context():
        #     session['username'] = 'testuser'

    def test_historical_endpoint_get(self):
        with patch.object(RelDBConnection, 'query_return_all_matches_with_parameter',
                          side_effect=mock_query_return_all_matches_with_parameter):
            with self.app.test_request_context():
                session['username'] = 'testuser'
                response = self.client.get('/historical')  # Use the correct endpoint
                self.assertEqual(response.status_code, 200)
                self.assertIn('historical_data', response.json)

    def test_historical_endpoint_get_specific_presentation(self):
        with patch.object(RelDBConnection, 'query_return_all_matches_with_parameter',
                          side_effect=mock_query_return_all_matches_with_parameter):
            response = self.client.get('/historical/specific/1')  # Adjust endpoint as necessary
            self.assertEqual(response.status_code, 200)  # Assuming download_presentation returns 200

    def test_historical_endpoint_delete_specific_presentation(self):
        with patch.object(RelDBConnection, 'query_return_all_matches_with_parameter',
                          side_effect=mock_query_return_all_matches_with_parameter), \
                patch.object(RelDBConnection, 'commit_query_with_parameter',
                             side_effect=mock_commit_query_with_parameter), \
                patch('src.utils.common_scripts.delete_file_of_type_specified',
                      side_effect=mock_delete_file_of_type_specified):
            response = self.client.delete('/historical/specific/1')  # Adjust endpoint as necessary
            self.assertEqual(response.status_code, 200)
            self.assertIn('Presentation deleted successfully', response.json.get('message', ''))


if __name__ == '__main__':
    unittest.main()
