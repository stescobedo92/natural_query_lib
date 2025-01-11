import asyncpg
from .exceptions import QueryExecutionError


class QueryExecutor:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.connection_string)

    async def execute(self, query: str, parameters: list = None):
        if not self.pool:
            raise QueryExecutionError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            try:
                return await connection.execute(query, *parameters)
            except Exception as e:
                raise QueryExecutionError(f"Error executing query: {e}")

    async def fetch(self, query: str, parameters: list = None):
        if not self.pool:
            raise QueryExecutionError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            try:
                return await connection.fetch(query, *parameters)
            except Exception as e:
                raise QueryExecutionError(f"Error fetching data: {e}")

    async def close(self):
        if self.pool:
            await self.pool.close()
