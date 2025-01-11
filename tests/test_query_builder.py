import pytest
from natural_query.query_builder import QueryBuilder, QueryType, JoinType


def test_select_query():
    query = (
        QueryBuilder(QueryType.SELECT)
        .from_table("users")
        .select_columns(["id", "name"])
        .where("age > 18")
        .build()
    )

    assert query == "SELECT id, name FROM users WHERE age > 18"


def test_join_query():
    query = (
        QueryBuilder(QueryType.SELECT)
        .from_table("users")
        .select_columns(["u.id", "o.order_date"])
        .join(JoinType.INNER, "orders o", "users.id = o.user_id")
        .build()
    )

    assert query == "SELECT u.id, o.order_date FROM users INNER JOIN orders o ON users.id = o.user_id"

