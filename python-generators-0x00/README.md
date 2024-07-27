# Python Generators: Task 0 - Getting Started with Python Generators

## Objective

Create a Python script (`seed.py`) that sets up a MySQL database and uses a generator to stream data row-by-row from a table.

---

## Description

This script performs the following:

- Connects to the MySQL server
- Creates a database named `ALX_prodev` if it doesn't already exist
- Creates a `user_data` table with the following fields:
    - `user_id` (UUID, Primary Key, Indexed)
    - `name` (VARCHAR, NOT NULL)
    - `email` (VARCHAR, NOT NULL)
    - `age` (DECIMAL, NOT NULL)
- Loads sample data from a `user_data.csv` file

---

## Files

- `seed.py`: Script for connecting, creating DB/tables, and seeding data
- `user_data.csv`: CSV file with sample user data (must be present in the same directory)
- `0-main.py`: Test script for running the seed file

---

## Functions

- `connect_db()`: Connect to MySQL without selecting a database
- `create_database(connection)`: Create the `ALX_prodev` database if not exists
- `connect_to_prodev()`: Connect to `ALX_prodev` database
- `create_table(connection)`: Create the `user_data` table
- `insert_data(connection, filename)`: Insert data into the table from CSV

---

## Sample Output

```bash
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
