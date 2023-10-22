import psycopg2
import sys
sys.path.append("../")
from logs.logging import logger

from config.config import DB_CONFIG

def create_tables():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the SQL schema script
        with open('schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()
            cursor.execute(schema_sql)
            conn.commit()

        logger.info('Database schema created successfully.')

        # Close the cursor and the connection
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f'Error creating database schema: {str(e)}')

if __name__ == '__main__':
    create_tables()
