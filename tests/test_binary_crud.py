
from pathlib import Path

from src.binary_database import BinaryDatabase


def main():

    database_name = "binary_crud_test"

    # Remove only this test database
    Path(
        f"data/{database_name}_schema.json"
    ).unlink(missing_ok=True)

    Path(
        f"data/{database_name}_employees.db"
    ).unlink(missing_ok=True)

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

    print("TEST 1: CREATE TABLE")

    db.create_table("employees", columns)

    print("\nTEST 2: INSERT RECORDS")

    employees = [
        {"id": 1, "name": "Arshad", "salary": 25000.0},
        {"id": 2, "name": "Rahul", "salary": 30000.0},
        {"id": 3, "name": "Amit", "salary": 35000.0}
    ]

    for employee in employees:
        db.insert("employees", employee)

    print("\nTEST 3: UPDATE RECORD")

    updated = db.update(
        "employees",
        {"id": 1},
        {"salary": 40000.0}
    )

    assert updated == 1

    print(db.select_all("employees"))

    print("\nTEST 4: DELETE RECORD")

    deleted = db.delete(
        "employees",
        {"id": 2}
    )

    assert deleted == 1

    print(db.select_all("employees"))

    print("\nTEST 5: VERIFY FINAL RECORDS")

    expected = [
        {"id": 1, "name": "Arshad", "salary": 40000.0},
        {"id": 3, "name": "Amit", "salary": 35000.0}
    ]

    actual = db.select_all("employees")

    assert actual == expected

    print("Final records:", actual)

    print("\nTEST 6: VERIFY PERSISTENCE")

    reopened_db = BinaryDatabase(database_name)

    recovered = reopened_db.select_all("employees")

    assert recovered == expected

    print("Records recovered successfully.")

    print("\nALL BINARY CRUD TESTS PASSED!")


if __name__ == "__main__":
    main()
