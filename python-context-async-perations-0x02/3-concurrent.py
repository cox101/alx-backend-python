#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = 'users.db'

async def async_fetch_users():
    """Fetch all users from the database asynchronously"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)
            return users

async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in users:
                print(user)
            return users

async def fetch_concurrently():
    """Run both fetch functions concurrently"""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
