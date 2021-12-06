class Nutrition:
    def __init__(
        self,
        protein: float,
        carbohydrates: float,
        fiber: float,
        fat: float,
        salt: float,
    ) -> None:
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fiber = fiber
        self.fat = fat
        self.salt = salt


class Cereal:
    def __init__(
        self, name: str, brand: str, price: float, grams: float, nutrition: Nutrition
    ) -> None:
        self.name = name
        self.brand = brand
        self.price = price
        self.grams = grams
        self.nutrition = nutrition
