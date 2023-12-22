import json
import mysql.connector

from src.database import queries


# MySQLConnection class
# This class is used to connect to a MySQL database
# It can be used to run queries with no return, with return, with parameters
# It can be used to run insert, update, delete, select
class MySQLConnection:

    # constructor for MySQLConnection class
    # reads in the host, user, password and database from the env_variables.json file
    def __init__(self):
        with open("./configs/env_variables.json", "r") as env_variables:
            env_variables = json.load(env_variables)
            self.host = env_variables["database"]["host"]
            self.user = env_variables["database"]["user"]
            self.password = env_variables["database"]["password"]
            self.database = env_variables["database"]["database"]

    def __str__(self):
        return (f"MySQLConnection(host={self.host}, user={self.user}, password={self.password}, "
                f"database={self.database})")

    # connect to the database
    # returns the connection
    def connect(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

    # run query with no return
    # useful for insert, update, delete
    def commit_query(self, passed_query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        connection.commit()
        connection.close()

    # run query with return. returns all rows
    # useful for select
    def query_return_all_matches(self, passed_query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchall()
        connection.close()
        return result

    # run query with return. returns first matching row
    # useful for select
    def query_return_first_match(self, passed_query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchone()
        connection.close()
        return result

    # run query with return. returns number of rows specified by size
    # useful for select
    def query_return_matches_specified(self, passed_query, size):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    # run query with a parameter and return all rows
    # useful for select
    def query_return_all_matches_with_parameter(self, passed_query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchall()
        connection.close()
        return result

    # run query with a parameter and return first match
    # useful for select
    def query_return_first_match_with_parameter(self, passed_query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchone()
        connection.close()
        return result

    # run query with a parameter and return number of rows specified by size
    # useful for select
    def query_return_matches_specified_with_parameter(self, passed_query, params, size):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    # run query with no return, with parameter
    # useful for insert, update, delete
    def commit_query_with_parameter(self, passed_query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(passed_query, params)
        connection.commit()
        connection.close()


if __name__ == '__main__':
    connect = MySQLConnection()
    query = queries.get_all_from_llm_table()
    print(connect.query_return_all_matches(query))
