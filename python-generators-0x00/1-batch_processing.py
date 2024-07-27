#!/usr/bin/env python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update if you have a password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:  # Yield remaining rows if they exist
            yield batch

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return


def batch_processing(batch_size):
    """Process batches of users, yielding only those over age 25."""
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user["age"] > 25:
                print(user)
