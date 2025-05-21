#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """Context manager that executes a given SQL query with parameters"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.connection = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()


# Usage Example
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery('users.db', query, params) as results:
        for row in results:
            print(row)

