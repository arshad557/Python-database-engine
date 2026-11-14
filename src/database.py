
from src.storage import Storage


class Database:

    def __init__(self, name):
        self.name = name
        self.storage = Storage(f"data/{name}.json")
        self.tables = self.storage.load()

        # Migrate previous list-based tables
        migrated = False

        for table_name, table in list(self.tables.items()):
            if isinstance(table, list):
                columns = []

                if table:
                    for key, value in table[0].items():
                        if isinstance(value, int) and not isinstance(value, bool):
                            data_type = "INT"
                        elif isinstance(value, float):
                            data_type = "FLOAT"
                        else:
                            data_type = "TEXT"

                        columns.append({
                            "name": key,
                            "type": data_type,
                            "primary_key": key == "id",
                            "not_null": key == "id"
                        })

                self.tables[table_name] = {
                    "columns": columns,
                    "records": table
                }
                migrated = True

        if migrated:
            self.storage.save(self.tables)

    def create_table(self, table_name, columns):

        if table_name in self.tables:
            print(f"Table '{table_name}' already exists.")
            return

        self.tables[table_name] = {
            "columns": columns,
            "records": []
        }

        self.storage.save(self.tables)
        print(f"Table '{table_name}' created successfully.")

    def validate_record(self, table_name, record):

        columns = self.tables[table_name]["columns"]

        expected = {column["name"] for column in columns}

        if set(record.keys()) != expected:
            raise ValueError("Record fields do not match table schema.")

        for column in columns:
            name = column["name"]
            value = record[name]
            data_type = column["type"]

            if value is None:
                if column["not_null"]:
                    raise ValueError(
                        f"Column '{name}' cannot be NULL."
                    )
                continue

            if data_type == "INT":
                valid = isinstance(value, int) and not isinstance(value, bool)

            elif data_type == "FLOAT":
                valid = isinstance(value, (int, float)) and not isinstance(value, bool)

            elif data_type == "TEXT":
                valid = isinstance(value, str)

            else:
                valid = False

            if not valid:
                raise ValueError(
                    f"Invalid data type for column '{name}'."
                )

    def insert(self, table_name, record):

        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        self.validate_record(table_name, record)

        columns = self.tables[table_name]["columns"]
        records = self.tables[table_name]["records"]

        primary_key = next(
            (c["name"] for c in columns if c["primary_key"]),
            None
        )

        if primary_key:
            for existing in records:
                if existing[primary_key] == record[primary_key]:
                    raise ValueError("Duplicate primary key.")

        records.append(record)
        self.storage.save(self.tables)

        print("Record inserted successfully.")

    def select_all(self, table_name, filters=None):

        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        records = self.tables[table_name]["records"]

        if filters is None:
            return [record.copy() for record in records]

        return [
            record.copy()
            for record in records
            if all(
                record.get(key) == value
                for key, value in filters.items()
            )
        ]

    def update(self, table_name, filters, updates):

        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        records = self.tables[table_name]["records"]
        columns = self.tables[table_name]["columns"]

        primary_key = next(
            (c["name"] for c in columns if c["primary_key"]),
            None
        )

        updated_records = []

        for record in records:
            candidate = record.copy()

            if all(
                record.get(key) == value
                for key, value in filters.items()
            ):
                candidate.update(updates)
                self.validate_record(table_name, candidate)
            updated_records.append(candidate)

        if primary_key:
            keys = [
                record[primary_key]
                for record in updated_records
            ]

            if len(keys) != len(set(keys)):
                raise ValueError("Duplicate primary key.")

        count = sum(
            1 for old, new in zip(records, updated_records)
            if old != new
        )

        self.tables[table_name]["records"] = updated_records
        self.storage.save(self.tables)

        print(f"{count} record(s) updated.")

    def delete(self, table_name, filters):

        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        records = self.tables[table_name]["records"]

        remaining = [
            record for record in records
            if not all(
                record.get(key) == value
                for key, value in filters.items()
            )
        ]

        deleted = len(records) - len(remaining)

        self.tables[table_name]["records"] = remaining
        self.storage.save(self.tables)

        print(f"{deleted} record(s) deleted.")
