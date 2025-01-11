import json
from typing import List, Optional, Any, Dict
from .enums import QueryType, JoinType
from .exceptions import QueryBuilderError


class QueryBuilder:
    def __init__(self, query_type: QueryType):
        self.query_type = query_type
        self.table = None
        self.columns = []
        self.conditions = []
        self.joins = []
        self.values = []
        self.params = []
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

    def where(self, condition: str, params: Optional[List[Any]] = None):
        self.conditions.append(condition)
        if params:
            self.params.extend(params)
        return self

    def join(self, join_type: JoinType, table: str, condition: str):
        self.joins.append((join_type.value, table, condition))
        return self

    def values_json(self, data: Dict[str, Any]):
        """Sets values for INSERT or UPDATE queries with JSON serialization."""
        for key, value in data.items():
            self.columns.append(key)
            self.values.append(json.dumps(value))
        return self

    def order_by_columns(self, columns: List[str]):
        self.order_by = columns
        return self

    def set_limit(self, limit: int):
        self.limit = limit
        return self

    def set_offset(self, offset: int):
        self.offset = offset
        return self

    def build(self) -> str:
        if not self.table:
            raise QueryBuilderError("Table name is required to build the query.")

        query = f"{self.query_type.value} "

        if self.query_type == QueryType.SELECT:
            columns = ", ".join(self.columns) if self.columns else "*"
            query += f"{columns} FROM {self.table} "

        elif self.query_type == QueryType.INSERT:
            cols = ", ".join(self.columns)
            placeholders = ", ".join(["%s"] * len(self.values))
            query += f"INTO {self.table} ({cols}) VALUES ({placeholders}) "

        elif self.query_type == QueryType.UPDATE:
            set_clauses = ", ".join([f"{col} = %s" for col in self.columns])
            query += f"{self.table} SET {set_clauses} "

        elif self.query_type == QueryType.DELETE:
            query += f"FROM {self.table} "

        if self.conditions:
            query += f"WHERE {' AND '.join(self.conditions)} "

        if self.order_by:
            query += f"ORDER BY {', '.join(self.order_by)} "

        if self.limit is not None:
            query += f"LIMIT {self.limit} "

        if self.offset is not None:
            query += f"OFFSET {self.offset} "

        return query.strip()

    def get_parameters(self) -> List[Any]:
        """Returns the list of parameters to bind dynamically."""
        return self.values + self.params
