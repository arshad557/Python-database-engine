
from src.parser import parse_query


class QueryEngine:

    def __init__(self, database):
        self.database = database

    def execute(self, query):

        parsed = parse_query(query)

        operation = parsed["operation"]
        table = parsed["table"]

        if operation == "CREATE":

            return self.database.create_table(
                table,
                parsed["columns"]
            )

        elif operation == "INSERT":

            return self.database.insert(
                table,
                parsed["record"]
            )

        elif operation == "SELECT":

            filters = parsed["filters"]

            # Use B-tree when filtering by the primary key
            if filters and hasattr(
                self.database,
                "find_by_primary_key"
            ):

                primary_key = self.database._get_primary_key(table)

                if (
                    primary_key is not None
                    and list(filters.keys()) == [primary_key]
                ):

                    record = self.database.find_by_primary_key(
                        table,
                        filters[primary_key]
                    )

                    return [] if record is None else [record]

            return self.database.select_all(
                table,
                filters
            )

        elif operation == "UPDATE":

            return self.database.update(
                table,
                parsed["filters"],
                parsed["updates"]
            )

        elif operation == "DELETE":

            return self.database.delete(
                table,
                parsed["filters"]
            )

        raise ValueError(
            f"Unsupported SQL operation: {operation}"
        )
