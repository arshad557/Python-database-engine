
from src.btree import BTree


def main():

    tree = BTree(degree=3)

    print("TEST 1: INSERT RECORDS")

    records = [
        (50, "Arshad"),
        (20, "Rahul"),
        (70, "Amit"),
        (10, "Priya"),
        (30, "Neha"),
        (60, "Karan"),
        (80, "Rohan"),
        (40, "Sneha"),
        (90, "Vijay"),
        (15, "Ankit"),
        (25, "Meera"),
        (35, "Sahil")
    ]

    for key, value in records:
        tree.insert(key, value)

    print("Inserted records:", len(tree))

    print("\nTEST 2: SEARCH")

    result = tree.search(50)

    print("Search key 50:", result)

    assert result == "Arshad"

    print("\nTEST 3: SEARCH MISSING KEY")

    result = tree.search(999)

    print("Search key 999:", result)

    assert result is None

    print("\nTEST 4: SORTED TRAVERSAL")

    sorted_records = tree.inorder()

    print(sorted_records)

    expected_keys = sorted(key for key, value in records)

    actual_keys = [key for key, value in sorted_records]

    assert actual_keys == expected_keys

    print("Keys are correctly sorted.")

    print("\nTEST 5: DUPLICATE KEY")

    try:
        tree.insert(50, "Duplicate")
    except ValueError as error:
        print("Correctly rejected:", error)
    else:
        raise AssertionError("Duplicate key was accepted.")

    print("\nTEST 6: SEARCH ALL RECORDS")

    for key, value in records:
        assert tree.search(key) == value

    print("All records found successfully.")

    print("\nALL B-TREE TESTS PASSED!")


if __name__ == "__main__":
    main()
