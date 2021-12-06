class Nutrition:
    """Nutritional content per 100 grams"""
    
    def __init__(self, protein, carbohydrates, fiber, fat, salt):
        """Initializes nutrition with protein, carbohydrates, fiber, fat, and salt"""
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fiber = fiber
        self.fat = fat
        self.salt = salt
        
class Cereal:
    """Cereal"""
    
    def __init__(self, name, brand, price, grams, nutrition):
        """Initializes cereal with name, brand, price, grams and nutrition"""
        self.name = name
        self.brand = brand
        self.price = price
        self.grams = grams
        self.nutrition = nutrition