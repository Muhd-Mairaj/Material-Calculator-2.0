from openpyxl.worksheet.worksheet import Worksheet


class Sheet():
    def __init__(self, ws: Worksheet) -> None:
        self._ws: Worksheet = ws
        self._setup()

    def _setup(self):
        self.header = self.ws[self.ws.min_row]

        self._profile_column = 0
        self._length_column = 0
        self._qty_column = 0
        for i, cell in enumerate(self.header, 1): # start at 1 because indexing is 1-based
            cell_value = cell.value
            if cell_value == None:
                continue

            elif cell_value.lower() == "profile":
                self._profile_column = i
            elif cell_value.lower() == "qty.":
                self._qty_column = i
            elif cell_value.lower() == "length":
                self._length_column = i


        profiles = set()
        for row in self.ws.iter_rows(min_row=self.ws.min_row+1, min_col=self._profile_column, max_col=self._profile_column):
            profiles.add(row[0].value)

        self._profiles = tuple(sorted(profiles))

    @property
    def ws(self):
        return self._ws

    @property
    def profiles(self):
        return self._profiles


if __name__ == "__main__":
    pass