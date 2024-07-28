import pytest
from material_calculator.calculator import Calculator


# for now this is just a dummy test to test functionality
def test_calculator(capfd):
    c = Calculator(12, {1000: 12})
    c.solve()

    out, err = capfd.readouterr()
    assert out == "solved\n"
    assert err == ""
