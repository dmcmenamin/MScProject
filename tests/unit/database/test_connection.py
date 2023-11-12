from unittest import TestCase
from unittest.mock import Mock
from src.database.connection import MySQLConnection


class TestMySQLConnection(TestCase):

    def setUp(self):
        # Create a mock for the MySQLConnection class
        self.mock_connection = Mock()
        self.connection = MySQLConnection("localhost", "root", "", "dynamicpowerpoint")
        # Override the connect method through the use of a lambda function, to not call the real database
        self.connection.connect = lambda: self.mock_connection

    # Perform a basic test to check that a connection is made
    def test_connect(self):
        connection = self.connection.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_commit_query(self):
        self.fail()

    def test_query_return_all_matches(self):
        cursor = self.mock_connection.cursor()
        cursor.execute.return_value = cursor
        cursor.fetchall.return_value = [[1, 'ChatGPT', '1000']]
        # self.mock_connection.cursor().execute.return_value = [[1, 'ChatGPT', '1000']]

        # Call the method to be tested
        results = self.connection.query_return_all_matches("SELECT * FROM llm_name")

        # Verify the result
        self.assertEqual(results, [[1, 'ChatGPT', '1000']])

    def test_query_return_first_match(self):
        self.fail()

    def test_query_return_matches_specified(self):
        self.fail()

    def test_query_return_all_matches_with_parameter(self):
        self.fail()

    def test_query_return_first_match_with_parameter(self):
        self.fail()

    def test_query_return_matches_specified_with_parameter(self):
        self.fail()

    def test_commit_query_with_parameter(self):
        self.fail()
