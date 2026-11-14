
import struct


class RecordSerializer:

    @staticmethod
    def serialize(record, columns):
        """
        Convert a Python dictionary into binary bytes.
        """

        result = bytearray()

        for column in columns:
            name = column["name"]
            data_type = column["type"]

            if name not in record:
                raise ValueError(f"Missing field: {name}")

            value = record[name]

            # NULL marker
            if value is None:
                if column.get("not_null", False):
                    raise ValueError(f"{name} cannot be NULL.")

                result.extend(b"\x00")
                continue

            result.extend(b"\x01")

            # Integer: 8 bytes
            if data_type == "INT":
                if isinstance(value, bool) or not isinstance(value, int):
                    raise ValueError(f"{name} must be an integer.")

                try:
                    result.extend(struct.pack(">q", value))
                except struct.error as error:
                    raise ValueError(f"Invalid integer in {name}.") from error

            # Float: 8 bytes
            elif data_type == "FLOAT":
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(f"{name} must be numeric.")

                result.extend(struct.pack(">d", float(value)))

            # Text: 4-byte length + UTF-8 bytes
            elif data_type == "TEXT":
                if not isinstance(value, str):
                    raise ValueError(f"{name} must be text.")

                text_bytes = value.encode("utf-8")

                result.extend(struct.pack(">I", len(text_bytes)))
                result.extend(text_bytes)

            else:
                raise ValueError(f"Unsupported type: {data_type}")

        return bytes(result)

    @staticmethod
    def deserialize(data, columns):
        """
        Convert binary bytes back into a Python dictionary.
        """

        offset = 0
        record = {}

        for column in columns:

            if offset >= len(data):
                raise ValueError("Incomplete record data.")

            marker = data[offset]
            offset += 1

            name = column["name"]
            data_type = column["type"]

            if marker == 0:
                if column.get("not_null", False):
                    raise ValueError(f"{name} cannot be NULL.")

                record[name] = None
                continue

            if marker != 1:
                raise ValueError("Invalid NULL marker.")

            if data_type == "INT":
                size = 8

                if offset + size > len(data):
                    raise ValueError("Incomplete integer data.")

                value = struct.unpack(
                    ">q", data[offset:offset + size]
                )[0]

                offset += size

            elif data_type == "FLOAT":
                size = 8

                if offset + size > len(data):
                    raise ValueError("Incomplete float data.")

                value = struct.unpack(
                    ">d", data[offset:offset + size]
                )[0]

                offset += size

            elif data_type == "TEXT":

                if offset + 4 > len(data):
                    raise ValueError("Incomplete text length.")

                length = struct.unpack(
                    ">I", data[offset:offset + 4]
                )[0]

                offset += 4

                if offset + length > len(data):
                    raise ValueError("Incomplete text data.")

                try:
                    value = data[offset:offset + length].decode("utf-8")
                except UnicodeDecodeError as error:
                    raise ValueError("Invalid UTF-8 data.") from error

                offset += length

            else:
                raise ValueError(f"Unsupported type: {data_type}")

            record[name] = value

        if offset != len(data):
            raise ValueError("Unexpected trailing record data.")

        return record
