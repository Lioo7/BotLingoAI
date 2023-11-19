# import sys

import psycopg2

# sys.path.append("../")
from logs.logging import logger


class PostgreSQL:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.database = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            print("Connected to PostgreSQL database")
            logger.info("Connected to PostgreSQL database")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            logger.error("Error while connecting to PostgreSQL:", error)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL database")

    def create_tables(self):
        if not self.connection:
            print("Not connected to the database.")
            return

        try:
            cursor = self.connection.cursor()

            # Execute the SQL schema script
            with open("database/schema.sql", "r") as schema_file:
                schema_sql = schema_file.read()
                cursor.execute(schema_sql)
                self.connection.commit()

            logger.info("Database schema created successfully.")
            print("Database schema created successfully.")

        except Exception as e:
            logger.error(f"Error creating database schema: {str(e)}")
            print(f"Error creating database schema: {str(e)}")
        finally:
            cursor.close()

    def save_user_to_db(self, first_name, phone_number="", email=""):
        if not self.connection:
            print("Not connected to the database.")
            return

        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO users (first_name, phone_number, email) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (first_name, phone_number, email))
            self.connection.commit()
            cursor.close()
            logger.info(
                f"Saving user: {first_name} | email: {email} to the database successful"
            )
            print(
                f"Saving user: {first_name} | email: {email} to the database successful"
            )
            return True
        except Exception as e:
            logger.error(f"Error saving user to the database: {str(e)}")
            print(f"Error saving user to the database: {str(e)}")
            return False

    def execute_query(self, query):
        if not self.connection:
            print("Not connected to the database.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
        finally:
            cursor.close()
