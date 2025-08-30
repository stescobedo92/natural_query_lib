# natural_query_lib

**natural_query_lib** is a lightweight Python library designed to simplify SQL query building and execution. It combines a fluent API with dynamic parameter binding and JSON support, making it easier for developers to work with SQL databases in an efficient and Pythonic way.

---

## 🚀 Features

- **Dynamic Query Building**: Supports `SELECT`, `INSERT`, `UPDATE`, and `DELETE` queries with a clean, fluent interface.
- **Dynamic Parameters**: Easily pass parameters to queries for security and flexibility.
- **JSON Encoding**: Seamless integration with JSON to handle complex data structures.
- **Asynchronous Execution**: Built-in support for async query execution using `asyncpg`.
- **Joins and Advanced Clauses**: Build queries with joins, grouping, ordering, and limits effortlessly.
- **Developer-Friendly**: Lightweight, easy-to-learn, and focused on productivity.

---

## 📦 Installation

Install the library directly from PyPI:

```bash
pip install natural_query_lib
```

---

## 🧪 Running Tests

To run the test suite and verify all query builder features:

```bash
pytest tests/
```

The tests cover:
- SELECT, INSERT, UPDATE, DELETE queries
- Joins, ordering, limits, offsets
- Grouping and having clauses
- Parameter binding and JSON value handling
- Error handling for missing table/columns

---

## 🛠️ Usage Examples

### **1. Build a Simple SELECT Query**

```python
from natural_query_lib import QueryBuilder, QueryType

query = (
    QueryBuilder(QueryType.SELECT)
    .from_table("users")
    .select_columns(["id", "name", "email"])
    .where("age > 18")
    .set_limit(10)
    .build()
)

print(query)  # Output: SELECT id, name, email FROM users WHERE age > 18 LIMIT 10
```

---

### **2. Execute Queries with Asyncpg**

```python
import asyncio
from natural_query_lib import QueryExecutor


async def main():
    executor = QueryExecutor("postgresql://user:password@localhost:5432/mydb")
    await executor.connect()

    query = "SELECT * FROM users WHERE age > $1"
    params = [18]

    results = await executor.fetch(query, params)
    for row in results:
        print(dict(row))

    await executor.close()


asyncio.run(main())
```

---

### **3. INSERT Data with JSON Support**

```python
from natural_query_lib import QueryBuilder, QueryType

query_builder = (
    QueryBuilder(QueryType.INSERT)
    .from_table("users")
    .select_columns(["name", "email", "profile"])
    .values_json({
        "name": "John Doe",
        "email": "john@example.com",
        "profile": {"age": 30, "location": "USA"}
    })
)

query = query_builder.build()
params = query_builder.get_parameters()

print(query)  # Output: INSERT INTO users (name, email, profile) VALUES (%s, %s, %s)
print(params)  # Output: ["John Doe", "john@example.com", '{"age": 30, "location": "USA"}']
```

---

### **4. Complex Query with Joins, Group By, and Having**

```python
from natural_query_lib import QueryBuilder, QueryType, JoinType

query = (
    QueryBuilder(QueryType.SELECT)
    .from_table("orders o")
    .select_columns(["o.id", "o.total", "u.name"])
    .join(JoinType.INNER, "users u", "o.user_id = u.id")
    .where("o.total > 100")
    .group_by_columns(["u.name"])
    .having_condition("SUM(o.total) > 1000")
    .order_by_columns(["o.total DESC"])
    .set_limit(5)
    .set_offset(10)
    .build()
)

print(query)
# Output: SELECT o.id, o.total, u.name FROM orders o INNER JOIN users u ON o.user_id = u.id WHERE o.total > 100 GROUP BY u.name HAVING SUM(o.total) > 1000 ORDER BY o.total DESC LIMIT 5 OFFSET 10
```

---

### **5. Error Handling Example**

```python
from natural_query_lib import QueryBuilder, QueryType, QueryBuilderError

try:
    query = QueryBuilder(QueryType.SELECT).select_columns(["id"]).build()
except QueryBuilderError as e:
    print("Error:", e)  # Output: Error: Table name is required to build the query.
```

---

## 🌟 Why Choose Natural Query?

### **✅ Fluent and Intuitive**
- Build queries step by step in a readable and maintainable manner.

### **✅ Secure and Dynamic**
- Parameterized queries help prevent SQL injection attacks.

### **✅ Asynchronous Execution**
- Leverages `asyncpg` for high-performance database interactions.

### **✅ JSON Ready**
- Easily handle JSON data structures without additional transformations.

### **✅ Lightweight**
- Minimal dependencies and optimized for performance.

---

## 🤝 Contributing

We welcome contributions to make **Natural Query** even better! Feel free to:
- Report bugs or suggest features by opening an [issue](https://github.com/tuusuario/natural-query/issues).
- Submit pull requests to improve functionality.

---

## 📜 License

**Natural Query** is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy coding! 🎉
