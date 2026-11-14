
from pathlib import Path


PAGE_SIZE = 4096


class PageFile:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path.touch(exist_ok=True)

    @property
    def page_count(self):
        file_size = self.file_path.stat().st_size
        return file_size // PAGE_SIZE

    def allocate_page(self):
        page_id = self.page_count

        with self.file_path.open("ab") as file:
            file.write(bytes(PAGE_SIZE))

        return page_id

    def write_page(self, page_id, data):

        if page_id < 0 or page_id >= self.page_count:
            raise ValueError("Invalid page ID.")

        if not isinstance(data, bytes):
            raise TypeError("Page data must be bytes.")

        if len(data) > PAGE_SIZE:
            raise ValueError("Data exceeds page size.")

        page_data = data.ljust(PAGE_SIZE, b"\x00")

        with self.file_path.open("r+b") as file:
            file.seek(page_id * PAGE_SIZE)
            file.write(page_data)

    def read_page(self, page_id):

        if page_id < 0 or page_id >= self.page_count:
            raise ValueError("Invalid page ID.")

        with self.file_path.open("rb") as file:
            file.seek(page_id * PAGE_SIZE)
            data = file.read(PAGE_SIZE)

        if len(data) != PAGE_SIZE:
            raise IOError("Incomplete page read.")

        return data
