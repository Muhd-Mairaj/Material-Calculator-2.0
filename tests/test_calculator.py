import pytest
from material_calculator.calculator import Calculator


# for now this is just a dummy test to test functionality
def test_calculator(capfd):
    c = Calculator(12000, {1000: 12})
    assert c._item_count == 12

    c = Calculator(12000, {1000: 12, 2000: 1})
    assert c._item_count == 13

    # test the .solve method
    # skipping this for now because its more tedious and needs more careful planning
