import sys

import psycopg2

sys.path.append("../")
from config.config import DB_CONFIG
from logs.logging import logger


def create_db_connection(config=DB_CONFIG):
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        logger.error(f"Error creating a database connection: {str(e)}")
        return None


def save_user_to_db(conn, first_name, phone_number="", email=""):
    try:
        cursor = conn.cursor()
        insert_query = (
            "INSERT INTO users (first_name, phone_number, email) VALUES (%s, %s, %s)"
        )
        cursor.execute(insert_query, (first_name, phone_number, email))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        logger.error(f"Error saving user to the database: {str(e)}")
        return False
