class StaticValues:
    def __init__(self, table_rows: int):
        self.ptr = 0
        self.table_row = 0
        self.current_step = 0
        self.table_rows = table_rows

    def increase_by_one(self, consumers_count):
        self.ptr = self.ptr + 1
        if self.ptr > consumers_count:
            self.ptr = 0
