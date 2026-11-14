
import json
import re
import os

from pathlib import Path

from src.page_store import PageFile
from src.page_manager import PageManager
from src.record_serializer import RecordSerializer
from src.btree import BTree


class BinaryDatabase:

    def __init__(self, name):

        if not re.fullmatch(r"[a-zA-Z_]\w*", name):
            raise ValueError("Invalid database name.")

        self.name = name
        self.data_dir = Path("data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_path = self.data_dir / f"{name}_schema.json"

        if self.metadata_path.exists():
            with self.metadata_path.open("r", encoding="utf-8") as file:
                self.tables = json.load(file)
        else:
            self.tables = {}

        # In-memory B-tree indexes
        self.indexes = {}

        # Rebuild indexes from binary files
        for table_name in self.tables:
            self._rebuild_index(table_name)

    def _save_metadata(self):

        with self.metadata_path.open("w", encoding="utf-8") as file:
            json.dump(self.tables, file, indent=4)

    def _validate_table_name(self, table_name):

        if not re.fullmatch(r"[a-zA-Z_]\w*", table_name):
            raise ValueError("Invalid table name.")

    def _get_page_manager(self, table_name):

        self._validate_table_name(table_name)

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        file_path = self.data_dir / f"{self.name}_{table_name}.db"

        page_file = PageFile(file_path)

        return PageManager(
            page_file,
            self.tables[table_name]["columns"]
        )

    def _get_primary_key(self, table_name):

        return next(
            (
                column["name"]
                for column in self.tables[table_name]["columns"]
                if column["primary_key"]
            ),
            None
        )

    def _validate_record(self, table_name, record):

        columns = self.tables[table_name]["columns"]

        RecordSerializer.serialize(record, columns)

    def _rebuild_index(self, table_name):

        manager = self._get_page_manager(table_name)

        primary_key = self._get_primary_key(table_name)

        if primary_key is None:
            self.indexes.pop(table_name, None)
            return

        tree = BTree(degree=3)

        records = manager.read_all_records()

        for record in records:

            key = record[primary_key]

            if tree.search(key) is not None:
                raise ValueError("Duplicate primary key in stored data.")

            tree.insert(key, record)

        self.indexes[table_name] = tree

    def create_table(self, table_name, columns):

        self._validate_table_name(table_name)

        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists.")

        if not columns:
            raise ValueError("A table must have columns.")

        names = [column["name"] for column in columns]

        if len(names) != len(set(names)):
            raise ValueError("Duplicate column names.")

        normalized_columns = []
        primary_keys = 0

        for column in columns:

            name = column["name"]
            data_type = column["type"].upper()

            if not re.fullmatch(r"[a-zA-Z_]\w*", name):
                raise ValueError(f"Invalid column name: {name}")

            if data_type not in ("INT", "FLOAT", "TEXT"):
                raise ValueError(f"Unsupported data type: {data_type}")

            primary_key = bool(column.get("primary_key", False))
            not_null = bool(column.get("not_null", False))

            if primary_key:
                primary_keys += 1
                not_null = True

            normalized_columns.append({
                "name": name,
                "type": data_type,
                "primary_key": primary_key,
                "not_null": not_null
            })

        if primary_keys > 1:
            raise ValueError("Only one primary key is supported.")

        self.tables[table_name] = {
            "columns": normalized_columns
        }

        self._save_metadata()

        self._get_page_manager(table_name)

        self._rebuild_index(table_name)

        print(f"Binary table '{table_name}' created successfully.")

    def insert(self, table_name, record):

        manager = self._get_page_manager(table_name)

        self._validate_record(table_name, record)

        primary_key = self._get_primary_key(table_name)

        if primary_key:

            key = record[primary_key]

            tree = self.indexes[table_name]

            if tree.search(key) is not None:
                raise ValueError("Duplicate primary key.")

        manager.append_record(record)

        # Update the in-memory index
        if primary_key:
            self.indexes[table_name].insert(
                record[primary_key],
                record
            )

        print("Record inserted successfully.")

    def select_all(self, table_name, filters=None):

        manager = self._get_page_manager(table_name)

        records = manager.read_all_records()

        if filters is None:
            return records

        return [
            record
            for record in records
            if all(
                record.get(key) == value
                for key, value in filters.items()
            )
        ]

    def find_by_primary_key(self, table_name, key):

        self._get_page_manager(table_name)

        primary_key = self._get_primary_key(table_name)

        if primary_key is None:
            raise ValueError("Table has no primary key index.")

        return self.indexes[table_name].search(key)

    def _rewrite_table(self, table_name, records):

        original_path = (
            self.data_dir / f"{self.name}_{table_name}.db"
        )

        temporary_path = (
            self.data_dir / f"{self.name}_{table_name}.tmp"
        )

        try:

            temporary_path.unlink(missing_ok=True)

            temporary_page_file = PageFile(temporary_path)

            manager = PageManager(
                temporary_page_file,
                self.tables[table_name]["columns"]
            )

            for record in records:
                manager.append_record(record)

            os.replace(temporary_path, original_path)

        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

    def update(self, table_name, filters, updates):

        manager = self._get_page_manager(table_name)

        if not filters:
            raise ValueError("UPDATE requires a filter.")

        if not updates:
            raise ValueError("No update values supplied.")

        columns = self.tables[table_name]["columns"]

        valid_names = {column["name"] for column in columns}

        if not set(updates).issubset(valid_names):
            raise ValueError("Unknown column in UPDATE.")

        if not set(filters).issubset(valid_names):
            raise ValueError("Unknown column in WHERE clause.")

        records = manager.read_all_records()

        updated_records = []
        updated_count = 0

        for record in records:

            candidate = record.copy()

            if all(
                record.get(key) == value
                for key, value in filters.items()
            ):

                candidate.update(updates)

                self._validate_record(table_name, candidate)

                updated_count += 1

            updated_records.append(candidate)

        primary_key = self._get_primary_key(table_name)

        if primary_key:

            keys = [
                record[primary_key]
                for record in updated_records
            ]

            if len(keys) != len(set(keys)):
                raise ValueError("Duplicate primary key.")

        if updated_count:

            self._rewrite_table(table_name, updated_records)

            self._rebuild_index(table_name)

        print(f"{updated_count} record(s) updated.")

        return updated_count

    def delete(self, table_name, filters):

        manager = self._get_page_manager(table_name)

        if not filters:
            raise ValueError("DELETE requires a filter.")

        columns = self.tables[table_name]["columns"]

        valid_names = {column["name"] for column in columns}

        if not set(filters).issubset(valid_names):
            raise ValueError("Unknown column in WHERE clause.")

        records = manager.read_all_records()

        remaining = [
            record for record in records
            if not all(
                record.get(key) == value
                for key, value in filters.items()
            )
        ]

        deleted_count = len(records) - len(remaining)

        if deleted_count:

            self._rewrite_table(table_name, remaining)

            self._rebuild_index(table_name)

        print(f"{deleted_count} record(s) deleted.")

        return deleted_count
