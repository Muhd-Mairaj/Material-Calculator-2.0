from .constants import MATERIAL_LENGTH
import copy


class Calculator:
    default_material_length = MATERIAL_LENGTH
    methods = ("Sort", "Adapted Sort")

    def __init__(self, items: dict[int, int], material_length: int = MATERIAL_LENGTH, method: str | None = None) -> None:
        """- material_length < 0 will use the default material length
        - For a list of available methods, print the methods class variable. Leave as None to use the preferred method.

        Args:
            items (dict[int, int]): A dictionary of item length to item quantity
            material_length (int, optional): The length of the material in mm.
            method (str | None, optional): The method to use for processing.
        """
        self._material_length: int = material_length if material_length >= 0 else MATERIAL_LENGTH
        self._items: dict[int, int] = items
        self._item_count: int = sum(self._items.values())
        self._method: str | None = method
        self._required: int | None = None
        self._scrap: int | None = None
        self._excess: int | None = None
        self._work_order: list[list[int]] | None = None

    @property
    def material_length(self) -> int:
        return self._material_length

    @property
    def items(self) -> dict:
        return dict(sorted(self._items.items(), reverse=True))

    @property
    def item_count(self) -> int:
        return self._item_count

    @property
    def method(self) -> str | None:
        return self._method

    @property
    def required(self) -> int:
        if self._required is None:
            self.solve()

        return self._required

    @property
    def scrap(self) -> int:
        if self._scrap is None:
            self.solve()

        return self._scrap

    @property
    def excess(self) -> int:
        if self._excess is None:
            self.solve()

        return self._excess

    @property
    def work_order(self) -> list[list[int]]:
        if self._work_order is None:
            self.solve()

        return copy.deepcopy(self._work_order)

    @property
    def results(self) -> tuple:
        return self.required, self.scrap, self.excess

    def solve(self) -> tuple[int, int, int]:
        """Calculates the results using the chosen method

        Returns:
            tuple[int, int, int]: (required, scrap, excess)
        """
        match self.method:
            # Sort method - uses a dictionary and goes through items in sorted manner
            case "Sort":
                return self._solve_sort()
            # Adapted Sort method - uses largest item first, then goes in reversed sorted manner
            case "Adapted Sort":
                return self._solve_adapted_sort()
            case _:
                return self._solve_preferred()

    def _solve_preferred(self) -> tuple[int, int, int]:
        return self._solve_sort()

    def _solve_sort(self) -> tuple[int, int, int]:
        print("\nUSING SORTING METHOD")

        self._required, self._scrap, self._excess = (0, 0, 0)
        self._work_order = []

        if self.item_count == 0:
            return (self._required, self._scrap, self._excess)

        self._required = 1    # will need at least 1
        cur_material_length = self.material_length
        cur_order = []
        num_items = self.item_count
        items_dict = self.items

        print(items_dict)
        while num_items >= 1:
            removed = False

            for item, count in items_dict.items():
                while cur_material_length - item >= 0 and count != 0:
                    cur_material_length -= item
                    cur_order.append(self.material_length-cur_material_length)
                    count -= 1
                    num_items -= 1
                    removed = True

                items_dict[item] = count

            if not removed:
                self._required += 1
                self._scrap += cur_material_length
                cur_material_length = 12000
                self._work_order.append(cur_order)
                cur_order = []

        self._excess = cur_material_length
        if cur_order:
            self._work_order.append(cur_order)

        return (self._required, self._scrap, self._excess)

    def _solve_adapted_sort(self) -> tuple[int, int, int]:
        print("\nUSING ADAPTED SORTING METHOD")

        self._required, self._scrap, self._excess = (0, 0, 0)
        self._work_order = []

        if self.item_count == 0:
            return (self._required, self._scrap, self._excess)

        self._required = 1  # will need at least 1
        cur_material_length = self.material_length
        cur_order = []
        num_items = self.item_count
        items_dict = self.items

        print(items_dict)
        print(dict(reversed(items_dict.items())))
        while num_items >= 1:
            removed = False

            for item, count in items_dict.items():
                while cur_material_length - item >= 0 and count != 0:
                    cur_material_length -= item
                    cur_order.append(self.material_length-cur_material_length)
                    count -= 1
                    num_items -= 1
                    removed = True

                items_dict[item] = count
                if removed:
                    break

            for item, count in reversed(items_dict.items()):
                while cur_material_length - item >= 0 and count != 0:
                    cur_material_length -= item
                    cur_order.append(self.material_length-cur_material_length)
                    count -= 1
                    num_items -= 1
                    removed = True

                items_dict[item] = count

            if not removed:
                self._required += 1
                self._scrap += cur_material_length
                cur_material_length = 12000
                self._work_order.append(cur_order)
                cur_order = []

        self._excess = cur_material_length
        if cur_order:
            self._work_order.append(cur_order)

        return (self._required, self._scrap, self._excess)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculator):
            raise TypeError

        assert (self.required*self.material_length-self.scrap-self.excess == other.required *
                other.material_length-other.scrap-other.excess), "EXAMINE THE CODE. VALUES DON'T ADD UP"

        return self.required == other.required and self.scrap == other.scrap and self.excess == other.excess

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Calculator):
            raise TypeError

        assert (self.required * self.material_length - self.scrap - self.excess
                == other.required * other.material_length - other.scrap - other.excess), "EXAMINE THE CODE. VALUES DON'T ADD UP"

        if self.required < other.required:
            return True

        if self.required == other.required and self.scrap < other.scrap:
            return True

        return False

    def print_stats(self, required=None, scrap=None, excess=None):
        # print(f"order of slice: {show_order}")
        required = required or self.required
        scrap = scrap or self.scrap
        excess = excess or self.excess
        print(f"\033[1;32;40mrequired raw material: {required}")
        print(f"total scrap: {scrap}")
        print(f"excess at the end: {excess}\033[1;37;40m \n")
