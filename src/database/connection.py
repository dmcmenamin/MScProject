import mysql.connector

from src.utils.common_scripts import get_environment_variables


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
        env_variables = get_environment_variables()

        self.host = env_variables["database"]["host"]
        self.user = env_variables["database"]["user"]
        self.password = env_variables["database"]["password"]
        self.database = env_variables["database"]["database"]
        self.connection_timeout = env_variables["database"]["connection_timeout"]

    def __str__(self):
        """ The string representation of the RelDBConnection class
        :return: The string representation of the RelDBConnection class
        """

        return (f"RelDBConnection(host={self.host}, user={self.user}, password={self.password}, "
                f"database={self.database}, connection_timeout={self.connection_timeout})")

    def connect(self):
        """ Connects to the database
        :return: The connection to the database, or an error if the connection fails
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                connection_timeout=self.connection_timeout
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

    def close_connection(self):
        """ Closes the connection to the database
        :return: None
        """
        self.connect().close()
