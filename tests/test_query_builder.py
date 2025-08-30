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


def test_insert_query():
    qb = QueryBuilder(QueryType.INSERT)
    qb.from_table("users").select_columns(["name", "email"]).values_json({"name": "Alice", "email": "alice@example.com"})
    query = qb.build()
    params = qb.get_parameters()
    assert query == "INSERT INTO users (name, email) VALUES (%s, %s)"
    assert params == ["Alice", "alice@example.com"]


def test_update_query():
    qb = QueryBuilder(QueryType.UPDATE)
    qb.from_table("users").select_columns(["name"]).values_json({"name": "Bob"}).where("id = %s", [1])
    query = qb.build()
    params = qb.get_parameters()
    assert query == "UPDATE users SET name = %s WHERE id = %s"
    assert params == ["Bob", 1]


def test_delete_query():
    qb = QueryBuilder(QueryType.DELETE)
    qb.from_table("users").where("id = %s", [2])
    query = qb.build()
    params = qb.get_parameters()
    assert query == "DELETE FROM users WHERE id = %s"
    assert params == [2]


def test_join_query():
    qb = QueryBuilder(QueryType.SELECT)
    qb.from_table("orders o").select_columns(["o.id", "u.name"]).join(QueryType.INNER, "users u", "o.user_id = u.id").where("o.total > 100")
    query = qb.build()
    assert "INNER JOIN users u ON o.user_id = u.id" in query


def test_order_limit_offset():
    qb = QueryBuilder(QueryType.SELECT)
    qb.from_table("users").order_by_columns(["name DESC"]).set_limit(5).set_offset(10)
    query = qb.build()
    assert "ORDER BY name DESC" in query
    assert "LIMIT 5" in query
    assert "OFFSET 10" in query


def test_group_by_having():
    qb = QueryBuilder(QueryType.SELECT)
    qb.from_table("sales").select_columns(["region", "SUM(amount)"]).group_by_columns(["region"]).having_condition("SUM(amount) > 1000")
    query = qb.build()
    assert "GROUP BY region" in query
    assert "HAVING SUM(amount) > 1000" in query


def test_missing_table_error():
    qb = QueryBuilder(QueryType.SELECT)
    try:
        qb.select_columns(["id"]).build()
        assert False, "Should have raised QueryBuilderError"
    except Exception as e:
        assert "Table name is required" in str(e)
