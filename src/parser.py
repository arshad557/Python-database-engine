
import re


IDENTIFIER = r"[A-Za-z_]\w*"

VALUE_PATTERN = (
    r"'(?:''|[^'])*'"
    r'|"(?:\\.|[^"])*"'
    r"|NULL"
    r"|-?\d+(?:\.\d+)?"
)


def parse_value(value):
    value = value.strip()

    if value.upper() == "NULL":
        return None

    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"')

    if re.fullmatch(r"-?\d+", value):
        return int(value)

    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)

    raise ValueError(f"Unsupported SQL value: {value}")


def split_values(text):
    """Split comma-separated values without splitting quoted strings."""

    values = []
    current = []
    quote = None
    index = 0

    while index < len(text):
        char = text[index]

        if quote:
            current.append(char)

            if char == quote:

                # SQL escaped single quote: ''
                if (
                    quote == "'"
                    and index + 1 < len(text)
                    and text[index + 1] == "'"
                ):
                    current.append(text[index + 1])
                    index += 1
                else:
                    quote = None

        elif char in ("'", '"'):
            quote = char
            current.append(char)

        elif char == ",":
            value = "".join(current).strip()

            if not value:
                raise ValueError("Empty SQL value.")

            values.append(value)
            current = []

        else:
            current.append(char)

        index += 1

    if quote:
        raise ValueError("Unclosed quotation mark.")

    final_value = "".join(current).strip()

    if not final_value:
        raise ValueError("Empty SQL value.")

    values.append(final_value)

    return values


def parse_query(query):

    query = query.strip()

    # CREATE TABLE
    match = re.fullmatch(
        rf"CREATE\s+TABLE\s+({IDENTIFIER})\s*"
        r"\((.*?)\)\s*;",
        query,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        table = match.group(1)
        definitions = split_values(match.group(2))
        columns = []

        for definition in definitions:

            parts = definition.strip().split()

            if len(parts) < 2 or len(parts) > 4:
                raise ValueError("Invalid column definition.")

            name = parts[0]
            data_type = parts[1].upper()

            constraints = " ".join(parts[2:]).upper()

            if not re.fullmatch(IDENTIFIER, name):
                raise ValueError("Invalid column name.")

            if data_type not in ("INT", "TEXT", "FLOAT"):
                raise ValueError("Unsupported data type.")

            if constraints not in ("", "PRIMARY KEY", "NOT NULL"):
                raise ValueError("Unsupported constraint.")

            columns.append({
                "name": name,
                "type": data_type,
                "primary_key": constraints == "PRIMARY KEY",
                "not_null": constraints in (
                    "PRIMARY KEY",
                    "NOT NULL"
                )
            })

        if not columns:
            raise ValueError("Table must contain columns.")

        if len({column["name"] for column in columns}) != len(columns):
            raise ValueError("Duplicate column names.")

        if sum(column["primary_key"] for column in columns) > 1:
            raise ValueError("Only one primary key is supported.")

        return {
            "operation": "CREATE",
            "table": table,
            "columns": columns
        }

    # SELECT
    match = re.fullmatch(
        rf"SELECT\s+\*\s+FROM\s+({IDENTIFIER})"
        rf"(?:\s+WHERE\s+({IDENTIFIER})\s*=\s*({VALUE_PATTERN}))?"
        r"\s*;",
        query,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        filters = None

        if match.group(2):
            filters = {
                match.group(2): parse_value(match.group(3))
            }

        return {
            "operation": "SELECT",
            "table": match.group(1),
            "filters": filters
        }

    # INSERT
    match = re.fullmatch(
        rf"INSERT\s+INTO\s+({IDENTIFIER})\s*"
        r"\((.*?)\)\s*VALUES\s*"
        r"\((.*?)\)\s*;",
        query,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        table = match.group(1)

        columns = [
            column.strip()
            for column in match.group(2).split(",")
        ]

        values = [
            parse_value(value)
            for value in split_values(match.group(3))
        ]

        if len(columns) != len(values):
            raise ValueError("Column and value counts do not match.")

        if len(set(columns)) != len(columns):
            raise ValueError("Duplicate column names.")

        if not all(re.fullmatch(IDENTIFIER, column) for column in columns):
            raise ValueError("Invalid column name.")

        return {
            "operation": "INSERT",
            "table": table,
            "record": dict(zip(columns, values))
        }

    # UPDATE
    match = re.fullmatch(
        rf"UPDATE\s+({IDENTIFIER})\s+SET\s+"
        rf"({IDENTIFIER})\s*=\s*({VALUE_PATTERN})"
        rf"\s+WHERE\s+({IDENTIFIER})\s*=\s*({VALUE_PATTERN})\s*;",
        query,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        return {
            "operation": "UPDATE",
            "table": match.group(1),
            "updates": {
                match.group(2): parse_value(match.group(3))
            },
            "filters": {
                match.group(4): parse_value(match.group(5))
            }
        }

    # DELETE
    match = re.fullmatch(
        rf"DELETE\s+FROM\s+({IDENTIFIER})"
        rf"\s+WHERE\s+({IDENTIFIER})\s*=\s*({VALUE_PATTERN})\s*;",
        query,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        return {
            "operation": "DELETE",
            "table": match.group(1),
            "filters": {
                match.group(2): parse_value(match.group(3))
            }
        }

    raise ValueError("Invalid or unsupported SQL query.")
