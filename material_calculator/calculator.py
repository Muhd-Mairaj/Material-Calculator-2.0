class Calculator:
    def __init__(self, material_length: int, items: dict, method: str | None = None) -> None:
        self._material_length: int = material_length
        self._items: dict = items
        self._item_count: int = sum(self._items.values())
        self._method: str | None = method

    def get_material_length(self) -> int:
        return self._material_length

    def get_items(self) -> dict:
        return self._items.copy()

    def get_item_count(self) -> int:
        return self._item_count

    def get_method(self) -> str | None:
        return self._method

    def solve(self) -> list:
        match self.get_method():
            # Sort method - uses a dictionary and goes through items in sorted manner
            case "Sort":
                return self._solve_sort()
            # Adapted Sort method - uses largest item first, then goes in reversed sorted manner
            case "Adapted Sort":
                return self._solve_adapted_sort()
            case _:
                return self._solve_preferred()

    def _solve_preferred(self) -> list:
        return self._solve_sort()

    def _solve_sort(self) -> list:
        print("\nUSING SORTING METHOD")

        required, scrap, excess = (0, 0, 0)

        if self.get_item_count() == 0:
            return [required, scrap, excess]

        required = 1    # will need at least 1
        cur_material_length = self.get_material_length()
        num_items = self.get_item_count()
        items_dict = self.get_items()
        while num_items >= 1:
            removed = False

            for item, count in items_dict.items():
                while cur_material_length - item >= 0 and count != 0:
                    cur_material_length -= item
                    count -= 1
                    num_items -= 1
                    removed = True

                items_dict[item] = count

            if not removed:
                required += 1
                scrap += cur_material_length
                cur_material_length = 12000

        excess = cur_material_length

        return [required, scrap, excess]

    def _solve_adapted_sort(self) -> list:
        raise NotImplementedError
