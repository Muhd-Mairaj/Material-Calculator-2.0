
class Calculator:
    def __init__(self, material_length: int, items: dict) -> None:
        self.material_length = material_length
        self.items: dict = items
    
    def solve(self):
        print("solved")
