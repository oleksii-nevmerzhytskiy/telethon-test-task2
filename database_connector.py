import mysql.connector

class DatabaseConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, host, username, password, database, port):
        if not hasattr(self, 'connection'):
            self.host = host
            self.username = username
            self.password = password
            self.database = database
            self.port = port
            self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
                port=self.port
            )

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def find_bot_method(self, bot_id: int):
        cursor = self.connection.cursor()
        query = f'SELECT method FROM bots_table WHERE user_id = {bot_id} limit 1;'
        cursor.execute(query)
        for row in cursor.fetchall():
            cursor.close()
            return row[0]

        return None

    def close(self):
        if self.connection:
            self.connection.close()