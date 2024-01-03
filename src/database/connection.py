import json
import os

import mysql.connector

from src.database import queries


class RelDBConnection:
    """ The RelDBConnection class
    This class is used to connect to a MySQL database
    """

    # constructor for RelDBConnection class
    # reads in the host, user, password and database from the env_variables.json file
    def __init__(self):
        """ The constructor for the RelDBConnection class
        Reads in the host, user, password and database from the env_variables.json file
        """
        if __name__ == 'app':
            # for production purposes
            with open(".env_variables.json", "r") as env_variables:
                env_variables = json.load(env_variables)
        elif __name__ == "__main__":
            # for development purposes
            with open("./configs/env_variables.json", "r") as env_variables:
                env_variables = json.load(env_variables)
        else:
            # for testing purposes
            rel_abs_path = os.path.abspath(os.path.dirname(__file__))
            abs_path = os.path.join(rel_abs_path, "..\\..\\configs\\env_variables.json")
            with open(abs_path, "r") as env_variables:
                env_variables = json.load(env_variables)

        self.host = env_variables["database"]["host"]
        self.user = env_variables["database"]["user"]
        self.password = env_variables["database"]["password"]
        self.database = env_variables["database"]["database"]

    def __str__(self):
        """ The string representation of the RelDBConnection class
        :return: The string representation of the RelDBConnection class
        """

        return (f"RelDBConnection(host={self.host}, user={self.user}, password={self.password}, "
                f"database={self.database})")

    def connect(self):
        """ Connects to the database
        :return: The connection to the database, or an error if the connection fails
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as error:
            return error

    def commit_query(self, passed_query):
        """ Runs a query with no return and commits it
        :param passed_query: The query to be run
        :return: None
        """

        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        connection.commit()
        connection.close()

    def query_return_all_matches(self, passed_query):
        """ Runs a query with return and returns all rows
        :param passed_query: The query to be run
        :return: All rows from the query"""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchall()
        connection.close()
        return result

    def query_return_first_match(self, passed_query):
        """ Runs a query with return and returns the first matching row
        :param passed_query: The query to be run
        :return: The first matching row from the query
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchone()
        connection.close()
        return result

    def query_return_matches_specified(self, passed_query, size):
        """ Runs a query with return and returns the number of rows specified by size
        :param passed_query: The query to be run
        :param size: The number of rows to be returned
        :return: The number of rows specified by size
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    def query_return_all_matches_with_parameter(self, passed_query, params):
        """ Runs a query with a parameter and returns all rows
        :param passed_query: The query to be run
        :param params: The parameter to be used in the query
        :return: All rows from the query
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchall()
        connection.close()
        return result

    def query_return_first_match_with_parameter(self, passed_query, params):
        """ Runs a query with a parameter and returns the first matching row
        :param passed_query: The query to be run
        :param params: The parameter to be used in the query
        :return: The first matching row from the query
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchone()
        connection.close()
        return result

    def query_return_matches_specified_with_parameter(self, passed_query, params, size):
        """ Runs a query with a parameter and returns the number of rows specified by size
        :param passed_query: The query to be run
        :param params: The parameter to be used in the query
        :param size: The number of rows to be returned
        :return: The number of rows specified by size
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    def commit_query_with_parameter(self, passed_query, params):
        """ Runs a query with a parameter and commits it
        :param passed_query: The query to be run
        :param params: The parameter to be used in the query
        :return: None
        """

        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        connection.commit()
        connection.close()