
from pathlib import Path

from src.binary_database import BinaryDatabase


def main():

    database_name = "binary_integration_test"

    # Remove only this dedicated test database
    metadata_file = Path(
        f"data/{database_name}_schema.json"
    )

    metadata_file.unlink(missing_ok=True)

    for table_name in ["employees"]:
        binary_file = Path(
            f"data/{database_name}_{table_name}.db"
        )
        binary_file.unlink(missing_ok=True)

    # Initialize binary database
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

    print("TEST 1: CREATE BINARY TABLE")

    db.create_table("employees", columns)

    print("\nTEST 2: INSERT RECORDS")

    employees = [
        {"id": 1, "name": "Arshad", "salary": 25000.50},
        {"id": 2, "name": "Rahul", "salary": 30000.00},
        {"id": 3, "name": "Amit", "salary": None}
    ]

    for employee in employees:
        db.insert("employees", employee)

    print("\nTEST 3: SELECT ALL RECORDS")

    records = db.select_all("employees")

    for record in records:
        print(record)

    assert records == employees

    print("\nTEST 4: SELECT WITH FILTER")

    result = db.select_all(
        "employees",
        {"id": 2}
    )

    print(result)

    assert result == [employees[1]]

    print("\nTEST 5: PRIMARY KEY VALIDATION")

    try:
        db.insert(
            "employees",
            {"id": 1, "name": "Duplicate", "salary": 10000.0}
        )
    except ValueError as error:
        print("Correctly rejected:", error)
    else:
        raise AssertionError("Duplicate primary key was accepted.")

    print("\nTEST 6: PERSISTENCE AFTER RESTART")

    # Open the same database again
    reopened_db = BinaryDatabase(database_name)

    recovered_records = reopened_db.select_all("employees")

    print(recovered_records)

    assert recovered_records == employees

    print("\nTEST 7: VERIFY BINARY FILE")

    binary_file = Path(
        f"data/{database_name}_employees.db"
    )

    print("Binary file exists:", binary_file.exists())
    print("Binary file size:", binary_file.stat().st_size, "bytes")

    assert binary_file.exists()
    assert binary_file.stat().st_size % 4096 == 0

    print("\nALL BINARY DATABASE TESTS PASSED!")


if __name__ == "__main__":
    main()
