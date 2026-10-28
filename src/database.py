import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

load_dotenv()

def get_db_connection():
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "smart_campus_energy")
    
    # Using mysql+pymysql
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    
    try:
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None
