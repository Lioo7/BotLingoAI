-- Define the schema for the database tables

CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,
    CHECK (phone_number IS NOT NULL OR email IS NOT NULL)
);