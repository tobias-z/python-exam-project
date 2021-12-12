class Nutrition:
    """Nutritional content per 100 grams"""
    
    def __init__(self, calories, protein, carbohydrates, fiber, fat, salt):
        """Initializes nutrition with calories (in kcal), and protein, carbohydrates, fiber, fat, and salt (in g)"""
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fiber = fiber
        self.fat = fat
        self.salt = salt
        
    def get_nutrition_as_list(self):
        """Returns the nutritional content as a list"""
        return [self.calories, self.protein, self.carbohydrates, self.fiber, self.fat, self.salt]
        
class Cereal:
    """Cereal"""
    
    def __init__(self, name, brand, prices, grams, nutrition):
        """Initializes cereal with name, brand, prices, grams and nutrition.
        Prices is a dictionary with store: price_in_store"""
        self.name = name
        self.brand = brand
        self.prices = prices
        self.grams = grams
        self.nutrition = nutrition