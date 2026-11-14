
from pathlib import Path

from src.binary_database import BinaryDatabase
from src.query_engine import QueryEngine


def main():

    database_name = "sql_binary_test"

    # Reset only this dedicated test database
    Path(
        f"data/{database_name}_schema.json"
    ).unlink(missing_ok=True)

    Path(
        f"data/{database_name}_employees.db"
    ).unlink(missing_ok=True)

    # Connect SQL engine to binary database
    database = BinaryDatabase(database_name)
    engine = QueryEngine(database)

    print("TEST 1: CREATE TABLE")

    engine.execute("""
        CREATE TABLE employees (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            salary FLOAT
        );
    """)

    print("\nTEST 2: INSERT RECORDS")

    engine.execute("""
        INSERT INTO employees (id, name, salary)
        VALUES (1, 'Arshad', 25000.50);
    """)

    engine.execute("""
        INSERT INTO employees (id, name, salary)
        VALUES (2, 'Rahul', 30000.00);
    """)

    engine.execute("""
        INSERT INTO employees (id, name, salary)
        VALUES (3, 'Amit', 35000.00);
    """)

    print("\nTEST 3: SELECT ALL")

    records = engine.execute(
        "SELECT * FROM employees;"
    )

    for record in records:
        print(record)

    assert len(records) == 3

    print("\nTEST 4: SELECT USING PRIMARY KEY")

    result = engine.execute(
        "SELECT * FROM employees WHERE id = 2;"
    )

    print(result)

    assert len(result) == 1
    assert result[0]["name"] == "Rahul"

    print("\nTEST 5: UPDATE")

    engine.execute("""
        UPDATE employees
        SET salary = 45000.00
        WHERE id = 2;
    """)

    updated = engine.execute(
        "SELECT * FROM employees WHERE id = 2;"
    )

    print(updated)

    assert updated[0]["salary"] == 45000.0

    print("\nTEST 6: DELETE")

    engine.execute(
        "DELETE FROM employees WHERE id = 1;"
    )

    remaining = engine.execute(
        "SELECT * FROM employees;"
    )

    print(remaining)

    assert len(remaining) == 2

    print("\nTEST 7: DUPLICATE PRIMARY KEY")

    try:
        engine.execute("""
            INSERT INTO employees (id, name, salary)
            VALUES (2, 'Duplicate', 10000.00);
        """)
    except ValueError as error:
        print("Correctly rejected:", error)
    else:
        raise AssertionError("Duplicate primary key accepted.")

    print("\nTEST 8: PERSISTENCE AFTER REOPEN")

    reopened_database = BinaryDatabase(database_name)
    reopened_engine = QueryEngine(reopened_database)

    recovered = reopened_engine.execute(
        "SELECT * FROM employees;"
    )

    print(recovered)

    assert len(recovered) == 2
    assert recovered[0]["id"] == 2
    assert recovered[0]["salary"] == 45000.0

    print("\nALL SQL BINARY INTEGRATION TESTS PASSED!")


if __name__ == "__main__":
    main()
