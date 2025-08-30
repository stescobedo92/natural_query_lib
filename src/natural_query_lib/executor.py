import asyncpg
import logging
from .exceptions import QueryExecutionError


class QueryExecutor:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(self.connection_string)
            logging.info("Database connection pool initialized.")
        except Exception as e:
            logging.error(f"Error initializing connection pool: {e}")
            raise QueryExecutionError(f"Error initializing connection pool: {e}")

    async def execute(self, query: str, parameters: list = None):
        if not self.pool:
            raise QueryExecutionError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            try:
                if parameters:
                    return await connection.execute(query, *parameters)
                else:
                    return await connection.execute(query)
            except Exception as e:
                logging.error(f"Error executing query: {query} | {e}")
                raise QueryExecutionError(f"Error executing query: {query} | {e}")

    async def fetch(self, query: str, parameters: list = None):
        if not self.pool:
            raise QueryExecutionError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            try:
                if parameters:
                    return await connection.fetch(query, *parameters)
                else:
                    return await connection.fetch(query)
            except Exception as e:
                logging.error(f"Error fetching data: {query} | {e}")
                raise QueryExecutionError(f"Error fetching data: {query} | {e}")

    async def close(self):
        if self.pool:
            await self.pool.close()
            logging.info("Database connection pool closed.")
