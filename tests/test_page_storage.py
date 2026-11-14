
from pathlib import Path

from src.page_store import PageFile, PAGE_SIZE


def main():

    database_file = Path("data/page_storage_test.db")

    # Create page storage
    storage = PageFile(database_file)

    print("TEST 1: INITIAL PAGE COUNT")
    print("Pages:", storage.page_count)

    # Allocate first page
    print("\nTEST 2: ALLOCATE PAGE")

    page_id = storage.allocate_page()

    print("Allocated page ID:", page_id)
    print("Total pages:", storage.page_count)

    # Write data
    print("\nTEST 3: WRITE PAGE")

    message = b"My first database page"

    storage.write_page(page_id, message)

    print("Page written successfully.")

    # Read data
    print("\nTEST 4: READ PAGE")

    loaded_data = storage.read_page(page_id)

    print("Retrieved:", loaded_data.rstrip(b"\x00"))

    # Verify page size
    print("\nTEST 5: VERIFY PAGE SIZE")

    print("Expected:", PAGE_SIZE)
    print("Actual:", len(loaded_data))

    assert loaded_data.startswith(message)
    assert len(loaded_data) == PAGE_SIZE

    print("\nALL PAGE STORAGE TESTS PASSED!")


if __name__ == "__main__":
    main()
