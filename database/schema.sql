-- Define the schema for the database tables

CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);