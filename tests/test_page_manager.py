
from pathlib import Path

from src.page_store import PageFile, PAGE_SIZE
from src.page_manager import PageManager


def main():

    # Use a separate test database file
    test_file = Path("data/page_manager_test.db")

    # Reset only this dedicated test file
    test_file.unlink(missing_ok=True)

    # Define table schema
    columns = [
        {
            "name": "id",
            "type": "INT",
            "not_null": True
        },
        {
            "name": "name",
            "type": "TEXT",
            "not_null": True
        },
        {
            "name": "salary",
            "type": "FLOAT",
            "not_null": False
        }
    ]

    # Initialize storage
    page_file = PageFile(test_file)

    manager = PageManager(
        page_file,
        columns
    )

    print("TEST 1: INITIAL PAGE COUNT")
    print("Pages:", page_file.page_count)

    # Insert records
    print("\nTEST 2: APPEND RECORDS")

    records = [
        {
            "id": 1,
            "name": "Arshad",
            "salary": 25000.50
        },
        {
            "id": 2,
            "name": "Rahul",
            "salary": 30000.00
        },
        {
            "id": 3,
            "name": "Amit",
            "salary": None
        }
    ]

    for record in records:
        page_id = manager.append_record(record)
        print(f"Inserted {record['name']} into page {page_id}")

    print("\nTEST 3: PAGE COUNT")
    print("Total pages:", page_file.page_count)

    print("\nTEST 4: READ ALL RECORDS")

    recovered_records = manager.read_all_records()

    for record in recovered_records:
        print(record)

    print("\nTEST 5: DATA INTEGRITY")

    assert recovered_records == records

    print("All records match the originals.")

    print("\nTEST 6: PAGE SIZE")

    for page_id in range(page_file.page_count):
        page = page_file.read_page(page_id)

        print(
            f"Page {page_id}: {len(page)} bytes"
        )

        assert len(page) == PAGE_SIZE

    print("\nALL PAGE MANAGEMENT TESTS PASSED!")


if __name__ == "__main__":
    main()
