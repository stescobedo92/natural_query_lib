from src.natural_query_lib import QueryBuilder, QueryType


def test_select_query():
    query = (
        QueryBuilder(QueryType.SELECT)
        .from_table("users")
        .select_columns(["id", "name"])
        .where("age > 18")
        .build()
    )

    assert query == "SELECT id, name FROM users WHERE age > 18"