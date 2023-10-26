import pytest
import psycopg2
from database.database_utils import create_db_connection, save_user_to_db
from config.config import TEST_DB_CONFIG

# Define the database name and user from the test configuration
TEST_DB_NAME = TEST_DB_CONFIG['dbname']
TEST_DB_USER = TEST_DB_CONFIG['user']

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_test_database(request):
    # Establish a connection to the default database for administrative tasks
    admin_conn = psycopg2.connect(
        dbname='postgres', user=TEST_DB_USER, password='', host='localhost', port='5432'
    )

    # Drop the test database if it exists
    admin_conn.set_isolation_level(0)
    admin_cursor = admin_conn.cursor()
    admin_cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    admin_cursor.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    admin_cursor.close()

    # Close the administrative connection
    admin_conn.close()

@pytest.fixture
def test_db_connection():
    # Establish a connection to the test database before running the tests
    conn = create_db_connection(TEST_DB_CONFIG)
    yield conn
    # Close the connection after the tests
    conn.close()

def execute_schema_sql(test_db_connection):
    # Execute the schema.sql file to create the 'users' table in the test database
    with open('database/schema.sql', 'r') as schema_file:
        schema_sql = schema_file.read()
        cursor = test_db_connection.cursor()
        cursor.execute(schema_sql)
        test_db_connection.commit()
        cursor.close()

def test_create_db_connection():
    # Test creating a database connection
    conn = create_db_connection(TEST_DB_CONFIG)
    assert conn is not None

def test_save_user_to_db(test_db_connection):
    # Execute the schema.sql file to create the 'users' table
    execute_schema_sql(test_db_connection)

    # Test saving a user to the database
    first_name = "John"
    phone_number = "123-456-7890"
    email = "john@example.com"

    result = save_user_to_db(test_db_connection, first_name, phone_number, email)
    assert result is True

    # Verify that the data was saved by retrieving it from the database
    cursor = test_db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE first_name = %s", (first_name,))
    user = cursor.fetchone()
    cursor.close()

    assert user is not None
    assert user[1] == first_name
    assert user[2] == phone_number
    assert user[3] == email


if __name__ == "__main__":
    pytest.main()
