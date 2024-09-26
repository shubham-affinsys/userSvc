# sql alchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import datetime

import logging
logger = logging.getLogger("app")

def create_user(user_detail):
    # for creating connection string
    connection_str = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASS')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"

    query_insert_user = text("""
        INSERT INTO users (username, email, password, first_name, last_name, date_of_birth, profile_picture, is_active, is_staff, bio, phone_number)
        VALUES (:username, :email, :password, :first_name, :last_name, :date_of_birth, :profile_picture, :is_active, :is_staff, :bio, :phone_number)
        """)
    try:
        # engine = create_engine(getenv("POSTGRES_DB_URL"),echo=True)
        engine = create_engine(connection_str, echo=True)

        with engine.connect() as conn:
            db_response = conn.execute(query_insert_user,user_detail)
            conn.commit()
            logger.debug(f"user inserted to db --- db response: {db_response}")
            logger.info("user created")
            return db_response
    except Exception as e:
        logger.error(f"could not create user: {e}")
        return "could not create user"
    



# Function to create the users table
def create_table():
    # Define the SQL query for creating the table
    query_create_table = text("""
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        date_of_birth DATE,
        profile_picture VARCHAR(255),  
        is_active BOOLEAN DEFAULT TRUE,
        is_staff BOOLEAN DEFAULT FALSE,
        date_joined TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,  
        last_login TIMESTAMPTZ, 
        bio TEXT,
        phone_number VARCHAR(20),
        additional_data JSONB DEFAULT '{}' 
        );
    """)

    # Create the engine to connect to the PostgreSQL database
    connection_str = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASS')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
    engine = create_engine(connection_str, echo=True)

    # Use the connection to execute the create table query
    with engine.connect() as conn:
        conn.execute(query_create_table)  # No need to capture the result
        conn.commit()
        logger.info("Table 'users' created successfully.")

def get_user(id=None):  # Accept an optional id parameter
    connection_str = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASS')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"

    if id is None:  # Adjusted to handle None for fetching all users
        query = text("SELECT * FROM users;")
    else:
        query = text("SELECT * FROM users WHERE id = :id;")

    try:
        engine = create_engine(connection_str)

        with engine.connect() as conn:
            if id is None:
                db_res = conn.execute(query).fetchall()  # Fetch all users
            else:
                db_res = conn.execute(query, {'id': id}).fetchone()  # Fetch a single user by ID

            # Convert the result to a JSON-serializable format
            if id is None:
                # Assuming the columns in the users table are as follows:
                columns = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'profile_picture', 'is_active', 'is_verified', 'created_at', 'updated_at', 'bio', 'phone_number']
                user = [dict(zip(columns, row)) for row in db_res]  # Map each row to a dictionary
            else:
                user = dict(zip(columns, db_res)) if db_res else None  # Convert single result to a dictionary

            logger.debug(f"user fetched from db --- db response: ===> {user}")
            logger.info("users fetched from db success")
            user = convert_to_serializable(user)
            return user
    except Exception as e:
        logger.error(f"could not fetch user: {e}")
        return "could not fetch user"

    
def convert_to_serializable(data):
    """Convert non-serializable data types to serializable formats."""
    if isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, datetime.date):
        return data.isoformat()  # Convert date to ISO format string
    elif isinstance(data, datetime.datetime):
        return data.isoformat()  # Convert datetime to ISO format string
    else:
        return data  # Return the data as is if it's already serializable

# {
#     "username": "test_user",
#     "email": "test.user@example.com",
#     "password": "secure_password123",
#     "first_name": "Test",
#     "last_name": "User",
#     "date_of_birth": "1995-05-20",
#     "profile_picture": "https://example.com/test_user_profile.jpg",
#     "is_active": true,
#     "is_staff": false,
#     "bio": "Just a test user.",
#     "phone_number": "555-123-4567"
# }
