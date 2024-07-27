#!/usr/bin/env python3
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the query if it's passed as an argument
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
