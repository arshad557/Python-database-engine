
import struct

from src.page_store import PAGE_SIZE
from src.record_serializer import RecordSerializer


HEADER_SIZE = 4
RECORD_LENGTH_SIZE = 4


class PageManager:

    def __init__(self, page_file, columns):
        self.page_file = page_file
        self.columns = columns

    def _decode_page(self, page_data):
        """Read the records stored in one page."""

        if len(page_data) != PAGE_SIZE:
            raise ValueError("Invalid page size.")

        record_count = struct.unpack(
            ">I", page_data[:HEADER_SIZE]
        )[0]

        records = []
        offset = HEADER_SIZE

        for _ in range(record_count):

            if offset + RECORD_LENGTH_SIZE > PAGE_SIZE:
                raise ValueError("Invalid record length header.")

            record_length = struct.unpack(
                ">I",
                page_data[offset:offset + RECORD_LENGTH_SIZE]
            )[0]

            offset += RECORD_LENGTH_SIZE

            if record_length == 0:
                raise ValueError("Empty record found.")

            if offset + record_length > PAGE_SIZE:
                raise ValueError("Record exceeds page boundary.")

            binary_record = page_data[
                offset:offset + record_length
            ]

            record = RecordSerializer.deserialize(
                binary_record,
                self.columns
            )

            records.append(record)
            offset += record_length

        return records, offset

    def append_record(self, record):
        """Serialize a record and append it to a page."""

        binary_record = RecordSerializer.serialize(
            record,
            self.columns
        )

        entry = (
            struct.pack(">I", len(binary_record))
            + binary_record
        )

        if HEADER_SIZE + len(entry) > PAGE_SIZE:
            raise ValueError("Record is too large for one page.")

        # Allocate the first page if necessary
        if self.page_file.page_count == 0:
            self.page_file.allocate_page()
            self.page_file.write_page(
                0,
                struct.pack(">I", 0)
            )

        # Try to append to the last page
        page_id = self.page_file.page_count - 1
        page_data = self.page_file.read_page(page_id)

        _, used_space = self._decode_page(page_data)

        if used_space + len(entry) > PAGE_SIZE:

            page_id = self.page_file.allocate_page()

            page_data = bytes(PAGE_SIZE)
            used_space = HEADER_SIZE

        # Add the new record
        updated_page = bytearray(page_data)

        updated_page[used_space:used_space + len(entry)] = entry

        old_count = struct.unpack(
            ">I", updated_page[:HEADER_SIZE]
        )[0]

        updated_page[:HEADER_SIZE] = struct.pack(
            ">I", old_count + 1
        )

        self.page_file.write_page(
            page_id,
            bytes(updated_page)
        )

        return page_id

    def read_all_records(self):
        """Read every record from every page."""

        all_records = []

        for page_id in range(self.page_file.page_count):

            page_data = self.page_file.read_page(page_id)

            records, _ = self._decode_page(page_data)

            all_records.extend(records)

        return all_records
