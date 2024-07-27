#!/usr/bin/env python3
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Reuse the with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator based on SQL query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        print("Query not in cache. Executing and caching result.")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call: will use cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
