
from src.record_serializer import RecordSerializer


def main():

    # Define table schema
    columns = [
        {
            "name": "id",
            "type": "INT",
            "primary_key": True,
            "not_null": True
        },
        {
            "name": "name",
            "type": "TEXT",
            "primary_key": False,
            "not_null": True
        },
        {
            "name": "salary",
            "type": "FLOAT",
            "primary_key": False,
            "not_null": False
        }
    ]

    # Original Python record
    original_record = {
        "id": 1,
        "name": "Arshad",
        "salary": 25000.50
    }

    print("TEST 1: ORIGINAL RECORD")
    print(original_record)

    # Serialize
    print("\nTEST 2: SERIALIZATION")

    binary_data = RecordSerializer.serialize(
        original_record,
        columns
    )

    print("Binary data:", binary_data)
    print("Binary size:", len(binary_data), "bytes")

    # Deserialize
    print("\nTEST 3: DESERIALIZATION")

    recovered_record = RecordSerializer.deserialize(
        binary_data,
        columns
    )

    print("Recovered record:", recovered_record)

    # Verify correctness
    print("\nTEST 4: DATA INTEGRITY")

    assert recovered_record == original_record

    print("Original and recovered records match!")

    # Test NULL handling
    print("\nTEST 5: NULL VALUE")

    null_record = {
        "id": 2,
        "name": "Rahul",
        "salary": None
    }

    encoded_null = RecordSerializer.serialize(
        null_record,
        columns
    )

    decoded_null = RecordSerializer.deserialize(
        encoded_null,
        columns
    )

    print("Recovered NULL record:", decoded_null)

    assert decoded_null == null_record

    print("\nALL SERIALIZATION TESTS PASSED!")


if __name__ == "__main__":
    main()
