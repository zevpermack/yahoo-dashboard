import os
import psycopg2
from dotenv import load_dotenv

def local_connect():
    """ Connect to the PostgreSQL database server """
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Get database connection parameters from environment variables
        config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
        }

        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
