import sys

import psycopg2

sys.path.append("../")
from config.config import DB_CONFIG
from logs.logging import logger


def create_tables(config=DB_CONFIG):
    try:
        # Connect to the database
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Execute the SQL schema script
        with open("schema.sql", "r") as schema_file:
            schema_sql = schema_file.read()
            cursor.execute(schema_sql)
            conn.commit()

        logger.info("Database schema created successfully.")

        # Close the cursor and the connection
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database schema: {str(e)}")


if __name__ == "__main__":
    create_tables()
