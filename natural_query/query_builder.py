from typing import List, Optional, Dict, Any
from enum import Enum

class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class JoinType(Enum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"


class QueryBuilder:
    def __init__(self, query_type: QueryType):
        self.query_type = query_type
        self.table = None
        self.columns = []
        self.conditions = []
        self.joins = []
        self.values = []
        self.order_by = []
        self.group_by = []
        self.having = None
        self.limit = None
        self.offset = None

    def from_table(self, table: str):
        self.table = table
        return self

    def select_columns(self, columns: List[str]):
        self.columns = columns
        return self

    def where(self, condition: str):
        self.conditions.append(condition)
        return self

    def join(self, join_type: JoinType, table: str, condition: str):
        self.joins.append((join_type.value, table, condition))
        return self

    def order_by_columns(self, columns: List[str]):
        self.order_by = columns
        return self

    def group_by_columns(self, columns: List[str]):
        self.group_by = columns
        return self

    def having_condition(self, condition: str):
        self.having = condition
        return self

    def set_limit(self, limit: int):
        self.limit = limit
        return self

    def set_offset(self, offset: int):
        self.offset = offset
        return self

    def build(self) -> str:
        if not self.table:
            raise ValueError("Table name is required to build the query.")

        query = f"{self.query_type.value} "

        if self.query_type == QueryType.SELECT:
            columns = ", ".join(self.columns) if self.columns else "*"
            query += f"{columns} FROM {self.table} "

        # Joins
        for join_type, table, condition in self.joins:
            query += f"{join_type} {table} ON {condition} "

        # Conditions
        if self.conditions:
            query += f"WHERE {' AND '.join(self.conditions)} "

        # Group By
        if self.group_by:
            query += f"GROUP BY {', '.join(self.group_by)} "

        if self.having:
            query += f"HAVING {self.having} "

        # Order By
        if self.order_by:
            query += f"ORDER BY {', '.join(self.order_by)} "

        # Limit and Offset
        if self.limit is not None:
            query += f"LIMIT {self.limit} "

        if self.offset is not None:
            query += f"OFFSET {self.offset} "

        return query.strip()
