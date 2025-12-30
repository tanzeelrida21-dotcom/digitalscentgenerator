"""Database configuration for PostgreSQL connection"""

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'scentdb',
    'user': 'postgres',
    'password': '0000'
}

# Connection pool
connection_pool = None

def initialize_pool():
    """Initialize database connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            **DB_CONFIG
        )
        if connection_pool:
            print("Connection pool created successfully")
    except Exception as e:
        print(f"Error creating connection pool: {e}")

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = connection_pool.getconn()
        yield connection
    finally:
        if connection:
            connection_pool.putconn(connection)

def execute_query(query, params=None, fetch=False):
    """Execute a database query"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    conn.commit()
                    return result
                conn.commit()
                return True
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_many(query, data):
    """Execute multiple queries at once"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                conn.commit()
                return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
