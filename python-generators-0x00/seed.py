import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connect to MySQL server (no database specified yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Adjust if you have a password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Adjust if you have a password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX idx_user_id (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, filename):
    """Insert data from CSV file into user_data table."""
    cursor = connection.cursor()

    # Open CSV and read rows
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row.get('user_id') or str(uuid.uuid4())
            name = row.get('name')
            email = row.get('email')
            age = row.get('age')

            # Check if user_id already exists
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
            if cursor.fetchone() is None:
                try:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
                    connection.commit()
                except mysql.connector.Error as err:
                    print(f"Failed to insert data: {err}")
    cursor.close()
