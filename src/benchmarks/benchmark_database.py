
import io
import time
from contextlib import redirect_stdout
from pathlib import Path

from src.binary_database import BinaryDatabase


DATA_DIR = Path("data")

RECORD_COUNTS = [100, 1000, 5000]

BTREE_REPEATS = 1000
SCAN_REPEATS = 50


def clean_benchmark_files(database_name):

    # Remove only files belonging to this benchmark database
    files = [
        DATA_DIR / f"{database_name}_schema.json",
        DATA_DIR / f"{database_name}_employees.db",
        DATA_DIR / f"{database_name}_employees.tmp",
    ]

    for file_path in files:
        file_path.unlink(missing_ok=True)


def benchmark_database(record_count):

    database_name = f"benchmark_{record_count}"

    clean_benchmark_files(database_name)

    print(f"\n{'=' * 55}")
    print(f"BENCHMARK: {record_count} RECORDS")
    print(f"{'=' * 55}")

    # Initialize database
    database = BinaryDatabase(database_name)

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

    database.create_table("employees", columns)

    # INSERT BENCHMARK
    print("\n1. INSERT PERFORMANCE")

    start = time.perf_counter()

    # Suppress per-record success messages
    with redirect_stdout(io.StringIO()):

        for employee_id in range(1, record_count + 1):

            record = {
                "id": employee_id,
                "name": f"Employee_{employee_id}",
                "salary": float(20000 + employee_id)
            }

            database.insert("employees", record)

    insertion_time = time.perf_counter() - start

    print(f"Records inserted: {record_count}")
    print(f"Total insertion time: {insertion_time:.6f} seconds")
    print(
        f"Average insertion time: "
        f"{(insertion_time / record_count) * 1000:.6f} ms"
    )

    # Choose an existing record
    target_id = record_count // 2

    # BTREE SEARCH BENCHMARK
    print("\n2. B-TREE PRIMARY KEY SEARCH")

    start = time.perf_counter()

    for _ in range(BTREE_REPEATS):
        result = database.find_by_primary_key(
            "employees",
            target_id
        )

    btree_time = time.perf_counter() - start

    assert result is not None
    assert result["id"] == target_id

    btree_average = btree_time / BTREE_REPEATS

    print(f"Search operations: {BTREE_REPEATS}")
    print(f"Total time: {btree_time:.6f} seconds")
    print(f"Average lookup: {btree_average * 1000:.6f} ms")

    # FULL TABLE SCAN BENCHMARK
    print("\n3. FULL TABLE SCAN")

    start = time.perf_counter()

    for _ in range(SCAN_REPEATS):

        result = database.select_all(
            "employees",
            {"id": target_id}
        )

    scan_time = time.perf_counter() - start

    assert len(result) == 1
    assert result[0]["id"] == target_id

    scan_average = scan_time / SCAN_REPEATS

    print(f"Scan operations: {SCAN_REPEATS}")
    print(f"Total time: {scan_time:.6f} seconds")
    print(f"Average scan: {scan_average * 1000:.6f} ms")

    # DATABASE FILE SIZE
    print("\n4. STORAGE INFORMATION")

    binary_file = DATA_DIR / f"{database_name}_employees.db"

    file_size = binary_file.stat().st_size

    print(f"Binary database size: {file_size:,} bytes")
    print(f"Database size: {file_size / 1024:.2f} KB")

    # PERFORMANCE COMPARISON
    print("\n5. PERFORMANCE COMPARISON")

    if btree_average > 0:

        speedup = scan_average / btree_average

        print(f"B-tree lookup speed: {btree_average * 1000:.6f} ms")
        print(f"Full scan speed: {scan_average * 1000:.6f} ms")
        print(f"Measured lookup speedup: {speedup:.2f}x")

    return {
        "records": record_count,
        "insert_seconds": insertion_time,
        "btree_ms": btree_average * 1000,
        "scan_ms": scan_average * 1000,
        "size_kb": file_size / 1024
    }


def main():

    DATA_DIR.mkdir(exist_ok=True)

    results = []

    for count in RECORD_COUNTS:

        result = benchmark_database(count)

        results.append(result)

    # FINAL SUMMARY
    print("\n\n")
    print("=" * 85)
    print("FINAL DATABASE PERFORMANCE REPORT")
    print("=" * 85)

    print(
        f"{'Records':<12}"
        f"{'Insert (s)':<16}"
        f"{'B-tree (ms)':<16}"
        f"{'Scan (ms)':<16}"
        f"{'Size (KB)':<12}"
    )

    print("-" * 85)

    for result in results:

        print(
            f"{result['records']:<12}"
            f"{result['insert_seconds']:<16.6f}"
            f"{result['btree_ms']:<16.6f}"
            f"{result['scan_ms']:<16.6f}"
            f"{result['size_kb']:<12.2f}"
        )

    print("=" * 85)

    print("\nALL PERFORMANCE BENCHMARKS COMPLETED!")


if __name__ == "__main__":
    main()
