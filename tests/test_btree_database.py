
from pathlib import Path

from src.binary_database import BinaryDatabase


def main():

    database_name = "btree_integration_test"

    # Reset only this test database
    Path(
        f"data/{database_name}_schema.json"
    ).unlink(missing_ok=True)

    Path(
        f"data/{database_name}_employees.db"
    ).unlink(missing_ok=True)

    print("TEST 1: CREATE DATABASE")

    db = BinaryDatabase(database_name)

    columns = [
        {
            "name": "id",
            "type": "INT",
            "primary_key": True
        },
        {
            "name": "name",
            "type": "TEXT",
            "not_null": True
        },
        {
            "name": "salary",
            "type": "FLOAT"
        }
    ]

    db.create_table("employees", columns)

    print("\nTEST 2: INSERT EMPLOYEES")

    employees = [
        {"id": 10, "name": "Arshad", "salary": 25000.0},
        {"id": 20, "name": "Rahul", "salary": 30000.0},
        {"id": 30, "name": "Amit", "salary": 35000.0},
        {"id": 40, "name": "Priya", "salary": 40000.0},
        {"id": 50, "name": "Neha", "salary": 45000.0}
    ]

    for employee in employees:
        db.insert("employees", employee)

    print("\nTEST 3: SEARCH USING B-TREE")

    result = db.find_by_primary_key("employees", 30)

    print("Employee with ID 30:", result)

    assert result == employees[2]

    print("\nTEST 4: SEARCH MISSING KEY")

    result = db.find_by_primary_key("employees", 999)

    print("Missing employee:", result)

    assert result is None

    print("\nTEST 5: UPDATE AND VERIFY INDEX")

    db.update(
        "employees",
        {"id": 30},
        {"salary": 50000.0}
    )

    result = db.find_by_primary_key("employees", 30)

    print("Updated employee:", result)

    assert result["salary"] == 50000.0

    print("\nTEST 6: DELETE AND VERIFY INDEX")

    db.delete(
        "employees",
        {"id": 20}
    )

    result = db.find_by_primary_key("employees", 20)

    print("Deleted employee lookup:", result)

    assert result is None

    print("\nTEST 7: REBUILD INDEX AFTER REOPEN")

    reopened_db = BinaryDatabase(database_name)

    result = reopened_db.find_by_primary_key("employees", 30)

    print("Recovered employee:", result)

    assert result["salary"] == 50000.0

    assert reopened_db.find_by_primary_key("employees", 20) is None

    print("\nALL B-TREE DATABASE INTEGRATION TESTS PASSED!")


if __name__ == "__main__":
    main()
