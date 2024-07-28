from material_calculator.calculator import Calculator

def main():
    c = Calculator(12, {1000: 12})
    c.solve()

if __name__ == "__main__":
    main()