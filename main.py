
from src.database import Database
from src.query_engine import QueryEngine


db = Database("college_db")
engine = QueryEngine(db)

print("\nTEST 1: CREATE TABLE")

if "constraint_demo" not in db.tables:
    engine.execute("""
        CREATE TABLE constraint_demo (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            salary FLOAT
        );
    """)
else:
    print("Table already exists.")

print("\nTEST 2: VALID INSERT")

if not engine.execute(
    "SELECT * FROM constraint_demo WHERE id = 1;"
):
    engine.execute("""
        INSERT INTO constraint_demo (id, name, salary)
        VALUES (1, 'Arshad', 25000.50);
    """)
else:
    print("Test record already exists.")

print("\nTEST 3: SELECT")

print(engine.execute("SELECT * FROM constraint_demo;"))

print("\nTEST 4: DUPLICATE PRIMARY KEY")

try:
    engine.execute("""
        INSERT INTO constraint_demo (id, name, salary)
        VALUES (1, 'Rahul', 30000.0);
    """)
except ValueError as error:
    print("Correctly rejected:", error)

print("\nTEST 5: NOT NULL VALIDATION")

try:
    engine.execute("""
        INSERT INTO constraint_demo (id, name, salary)
        VALUES (2, NULL, 30000.0);
    """)
except ValueError as error:
    print("Correctly rejected:", error)

print("\nTEST 6: FINAL RECORDS")

print(engine.execute("SELECT * FROM constraint_demo;"))
