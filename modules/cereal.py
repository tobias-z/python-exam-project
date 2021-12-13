class Nutrition:
    """Nutritional content per 100 grams"""
    
    def __init__(self, protein, carbohydrates, fiber, fat, salt, calories):
        """Initializes nutrition with calories (in kcal), and protein, carbohydrates, fiber, fat, and salt (in g)"""
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fiber = fiber
        self.fat = fat
        self.salt = salt
        self.calories = calories
        
    def get_nutrition_as_list(self):
        """Returns the nutritional content as a list"""
        return [self.calories, self.protein, self.carbohydrates, self.fiber, self.fat, self.salt]
        
class Cereal:
    """Cereal"""
    
    def __init__(self, name, brand, price, grams, is_original, nutrition):
        """Initializes cereal with name, brand, prices, grams and nutrition.
        Price is a dictionary with store: price_in_store"""
        self.name = name
        self.brand = brand
        self.price = price
        self.grams = grams
        self.is_original = is_original
        self.nutrition = nutrition
        
    def __str__(self):
        return 'Cereal: %s %s costs: %r.\nNutrition: %r' % (self.brand, self.name, self.price, self.nutrition)