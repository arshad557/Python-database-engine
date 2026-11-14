# Python Database Engine

A custom database engine developed using Python, implementing SQL query processing, binary file storage, page management, record serialization, and B-tree indexing.

## Project Overview

This project demonstrates the internal working of a database management system by implementing its core components from scratch.

Instead of relying on an existing database engine, it uses custom-built modules to process supported SQL statements, manage records, store data in binary files, and retrieve records using B-tree indexing.

## Key Features

- Custom SQL query parser
- SQL query execution engine
- CREATE TABLE, INSERT, SELECT, UPDATE and DELETE operations
- Binary file-based data storage
- Fixed-size 4096-byte database pages
- Record serialization and deserialization
- Page management
- B-tree indexing
- Primary-key validation and duplicate detection
- Data persistence after reopening the database
- Performance benchmarking

## Technology Stack

- Python
- SQL
- Regular Expressions
- Binary File Handling
- Data Structures and Algorithms
- B-tree Indexing
- JSON Metadata Storage
- Unit and Integration Testing

## Project Architecture

SQL Query → SQL Parser → Query Engine → Binary Database → Page Manager → Page Storage

The B-tree index supports primary-key lookups.

## Project Structure

```text
Python-Database-Engine/
│
├── data/
├── docs/
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
├── main.py
└── README.md
```

## Testing

The project includes separate tests for:

- Page storage
- Record serialization
- Page management
- Binary database operations
- Binary CRUD operations
- B-tree operations
- B-tree database integration
- SQL-to-binary database integration

## Performance Benchmark

The database was benchmarked using different record counts.

| Records | Insert Time (seconds) | B-tree Lookup (ms) | Full Scan (ms) | Storage (KB) |
|---:|---:|---:|---:|---:|
| 100 | 0.221547 | 0.593929 | 1.964122 | 4 |
| 1,000 | 2.959015 | 0.612793 | 6.205474 | 40 |
| 5,000 | 12.266342 | 1.025043 | 62.770714 | 196 |

*Results from the current development environment; performance may vary across systems.*

## How to Run

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Python-Database-Engine
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Run the application:

```bash
python main.py
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