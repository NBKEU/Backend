# File: database/database.py
# This is a production-ready database interaction layer using PostgreSQL.

import os
import logging
import psycopg2
from psycopg2 import Error

logger = logging.getLogger(__name__)

# --- Database Connection and Credential Management ---
# Credentials should be set as environment variables on Render.
DB_NAME = os.environ.get('DB_NAME', 'your_db_name')
DB_USER = os.environ.get('DB_USER', 'your_db_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_db_password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logger.info("Database connection successful")
        return conn
    except Error as e:
        logger.error(f"Error connecting to PostgreSQL database: {e}")
        return None

def setup_database():
    """
    Creates the transactions table if it doesn't exist.
    This function should be called once on application startup.
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        protocol VARCHAR(255) NOT NULL,
                        amount NUMERIC(10, 2) NOT NULL,
                        auth_code VARCHAR(255) NOT NULL,
                        transaction_type VARCHAR(50) NOT NULL,
                        status VARCHAR(50) NOT NULL,
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        tx_hash VARCHAR(255)
                    );
                """)
            conn.commit()
            logger.info("Transactions table created or already exists.")
        except Error as e:
            logger.error(f"Error setting up database: {e}")
        finally:
            conn.close()

def save_transaction(protocol, amount, auth_code, transaction_type, status, tx_hash=None):
    """
    Saves a transaction record to the PostgreSQL database.
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO transactions (protocol, amount, auth_code, transaction_type, status, tx_hash)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (protocol, amount, auth_code, transaction_type, status, tx_hash))
            conn.commit()
            logger.info("Transaction successfully saved to PostgreSQL.")
            return True
        except Error as e:
            logger.error(f"Error saving transaction: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    return False

def get_transaction_history():
    """
    Retrieves the full transaction history from the PostgreSQL database.
    """
    conn = get_db_connection()
    history = []
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM transactions ORDER BY timestamp DESC;")
                columns = [desc[0] for desc in cur.description]
                for row in cur.fetchall():
                    history.append(dict(zip(columns, row)))
            logger.info("Transaction history retrieved from PostgreSQL.")
        except Error as e:
            logger.error(f"Error retrieving transaction history: {e}")
        finally:
            conn.close()
    return history
