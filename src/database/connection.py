import mysql.connector


# MySQLConnection class
# This class is used to connect to a MySQL database
# It can be used to run queries with no return, with return, with parameters
# It can be used to run insert, update, delete, select
class MySQLConnection:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __str__(self):
        return f"MySQLConnection(host={self.host}, user={self.user}, password={self.password}, database={self.database})"

    def connect(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

    # run query with no return
    # useful for insert, update, delete
    def commit_query(self, query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    # run query with return. returns all rows
    # useful for select
    def query_return_all_matches(self, query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    # run query with return. returns first matching row
    # useful for select
    def query_return_first_match(self, query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        return result

    # run query with return. returns number of rows specified by size
    # useful for select
    def query_return_matches_specified(self, query, size):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    # run query with a parameter and return all rows
    # useful for select
    def query_return_all_matches_with_parameter(self, query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.close()
        return result

    # run query with a parameter and return first match
    # useful for select
    def query_return_first_match_with_parameter(self, query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        connection.close()
        return result

    # run query with a parameter and return number of rows specified by size
    # useful for select
    def query_return_matches_specified_with_parameter(self, query, params, size):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchmany(size)
        connection.close()
        return result

    # run query with no return, with parameter
    # useful for insert, update, delete
    def commit_query_with_parameter(self, query, params):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()


if __name__ == '__main__':
    connect = MySQLConnection("localhost", "root", "", "dynamicpowerpoint")
    print(connect.query_return_all_matches("SELECT * FROM llm_details"))




