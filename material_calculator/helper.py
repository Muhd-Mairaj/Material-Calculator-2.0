from .calculator import Calculator

def check_which_better(calculators: tuple[Calculator, Calculator]) -> str:
    """Checks which method did better and returns the method name"""

    calc1, calc2 = calculators
    best = _check_better(calc1, calc2)
    return best.method if best else "Same"
        
    # return_value = ""

def _check_better(calc1: Calculator, calc2: Calculator):
    best = None
    if calc1.required == calc2.required:
        if calc1.scrap + (calc1.excess - calc2.excess) == calc2.scrap:
            if calc2.scrap > calc1.scrap and calc1.excess > calc2.excess:
                best = calc1

            elif calc1.scrap > calc2.scrap and calc2.excess > calc1.excess:
                best = calc2

            elif calc1.scrap == calc2.scrap and calc1.excess == calc2.excess:
                best = None

            else:
                assert (
                    calc1.scrap + (calc1.excess - calc2.excess) == calc2.scrap
                ), "EXAMINE THE CODE. VALUES DON'T ADD UP *1*"

        else:
            assert (
                calc1.scrap + (calc1.excess - calc2.excess) == calc2.scrap
            ), "EXAMINE THE CODE. VALUES DON'T ADD UP *2*"

    elif calc1.required < calc2.required:
        best = calc1

    elif calc1.required > calc2.required:
        best = calc2
    
    return best



    # if required1 == required2:

    #     if calc1.scrap + (excess1 - excess2) == scrap2:
    #         if scrap2 > calc1.scrap and excess1 > excess2:
    #             return_value = "Sort method"

    #         elif calc1.scrap > scrap2 and excess2 > excess1:
    #             return_value = "Adopted Sort method"

    #         elif calc1.scrap == scrap2 and excess1 == excess2:
    #             return_value = "Same"

    #         else:
    #             assert (
    #                 calc1.scrap + (excess1 - excess2) == scrap2
    #             ), "EXAMINE THE CODE. VALUES DON'T ADD UP *1*"

    #     else:
    #         assert (
    #             calc1.scrap + (excess1 - excess2) == scrap2
    #         ), "EXAMINE THE CODE. VALUES DON'T ADD UP *2*"

    # elif required1 < required2:
    #     return_value = "Sort method"

    # elif required1 > required2:
    #     return_value = "Adopted Sort method"

    # return return_value
