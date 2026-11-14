# Python Database Engine

A custom database management system (DBMS) developed from scratch using Python. It implements SQL query processing, binary file storage, fixed-size database pages, record serialization, page management, and B-tree indexing.

## Project Overview

This project demonstrates the internal working of a database management system by implementing its core components from scratch.

Instead of relying on an existing database engine, it uses custom-built modules to parse supported SQL statements, execute database operations, manage records, store data in binary files, and retrieve records using B-tree indexing.

## Key Features

- Custom SQL query parser
- SQL query execution engine
- CREATE TABLE, INSERT, SELECT, UPDATE and DELETE operations
- Binary file-based data storage
- Fixed-size 4096-byte database pages
- Record serialization and deserialization
- Page management
- B-tree indexing for primary-key lookups
- Primary-key validation and duplicate detection
- Data persistence after reopening the database
- Performance benchmarking

## Technology Stack

- **Language:** Python
- **Query Language:** SQL (supported subset)
- **Data Structures:** B-tree
- **Storage:** Binary file handling
- **Metadata:** JSON
- **Parsing:** Regular Expressions
- **Testing:** Custom unit and integration test modules
- **Version Control:** Git and GitHub

## System Architecture

The database engine follows a modular architecture:

```text
             User / SQL Query
                    |
                    v
               SQL Parser
                    |
                    v
              Query Engine
                    |
                    v
             Binary Database
                    |
          +---------+---------+
          |                   |
          v                   v
     Page Manager         B-tree Index
          |
          v
       Page Store
          |
          v
     Binary Database File
```

The SQL parser converts supported SQL statements into structured operations. The query engine forwards these operations to the database layer. The database manages records through page storage and uses an in-memory B-tree index for primary-key lookups.

## Project Structure

```text
Python-Database-Engine/
│
├── data/
│   └── Generated database files
│
├── docs/
│   └── architecture.md
│
├── src/
│   ├── database.py
│   ├── binary_database.py
│   ├── btree.py
│   ├── page_manager.py
│   ├── page_store.py
│   ├── record_serializer.py
│   ├── parser.py
│   ├── query_engine.py
│   └── storage.py
│
├── tests/
│   ├── test_page_storage.py
│   ├── test_record_serializer.py
│   ├── test_page_manager.py
│   ├── test_binary_database.py
│   ├── test_binary_crud.py
│   ├── test_btree.py
│   ├── test_btree_database.py
│   └── test_sql_binary.py
│
├── src/benchmarks/
│   └── benchmark_database.py
│
├── main.py
├── README.md
└── .gitignore
```

## Supported SQL Operations

The engine currently supports the following SQL operations:

### Create Table

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    salary FLOAT
);
```

### Insert Records

```sql
INSERT INTO employees (id, name, salary)
VALUES (1, 'Arshad', 25000.5);
```

### Select Records

```sql
SELECT * FROM employees;
```

### Update Records

```sql
UPDATE employees
SET salary = 40000
WHERE id = 1;
```

### Delete Records

```sql
DELETE FROM employees
WHERE id = 1;
```

*Note: These examples illustrate the supported SQL subset, not full SQL compatibility.*

## Testing

The project includes separate test modules for:

- Page storage
- Record serialization
- Page management
- Binary database operations
- Binary CRUD operations
- B-tree operations
- B-tree database integration
- SQL-to-binary database integration

Run individual test modules from the project root:

```powershell
python -m tests.test_page_storage
python -m tests.test_record_serializer
python -m tests.test_page_manager
python -m tests.test_binary_database
python -m tests.test_binary_crud
python -m tests.test_btree
python -m tests.test_btree_database
python -m tests.test_sql_binary
```

## Performance Benchmark

The database was benchmarked using different record counts.

| Records | Insert Time (seconds) | B-tree Lookup (ms) | Full Scan (ms) | Storage (KB) |
|---:|---:|---:|---:|---:|
| 100 | 0.221547 | 0.593929 | 1.964122 | 4 |
| 1,000 | 2.959015 | 0.612793 | 6.205474 | 40 |
| 5,000 | 12.266342 | 1.025043 | 62.770714 | 196 |

*Results from the current development environment. Performance may vary depending on hardware and system conditions.*

The benchmark illustrates the difference between indexed primary-key lookup and full-record scanning for the tested datasets.

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/arshad557/Python-database-engine.git
cd Python-database-engine
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment (Windows)

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Run the application

```powershell
python main.py
```

### 5. Run the benchmark

```powershell
python -m src.benchmarks.benchmark_database
```

## Future Enhancements

- Additional SQL operations and query capabilities
- Multi-column indexing
- Query optimization
- Transaction management
- Concurrent database access
- Recovery and crash-safety mechanisms

## Author

Developed as a hands-on database systems and software engineering project.

**GitHub:** https://github.com/arshad557