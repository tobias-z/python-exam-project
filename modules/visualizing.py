from IPython.display import display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show_prices(cereals, per_100g=False):
    """Creates and displays a bar chart over cereal prices
    
    Parameters:
    cereals: List of Cereal objects
    per_100g: Boolean. True, if the bar chart should be per 100 grams for easier comparison. Default False
    """
    #names = [cereal.get_brand_name() for cereal in cereals]
    #stores = __get_stores(cereals)
    #prices_in_stores = __get_prices_with_cereal_name(stores, cereals)
    #title = 'Cereal Prices'
    #__plot_prices(names, stores, prices_in_stores, title)
    stores = list(__get_stores(cereals))
    for store in stores:
        title = __create_title(store, per_100g)
        cereals_prices = {cereal.get_brand_name(): __get_price(value, cereal.grams, per_100g) for cereal in cereals 
                            for key, value in cereal.price.items() if key == store}
        __plot_prices_in_store(cereals_prices, title)
        
def show_nutrition(cereals):
    """Creates and displays a dataframe over the nutritional content
    (protein, carbohydrates, fiber, fat, salt)
    per 100 grams in cereals
    
    Parameters:
    cereals: List of Cereal objects
    """
    data = __get_nutrition_data(cereals)
    df = pd.DataFrame(data)
    print('Nutritional Content per 100 grams in Cereals')
    #df = df.style.set_caption('Nutritional Content per 100 grams in Cereals')
    display(df)
    
def show_recommended_nutrition():
    """Creates and displays a dataframe over the daily recommended maximum nutritional intake
    (protein, carbohydrates, fiber, fat, salt)
    """
    df = __get_recommended_nutrition()
    print('Daily Recommended Maximum Nutritional Intake')
    #df = df.style.set_caption('Daily Recommended Nutritional Intake')
    display(df)
    
def show_pct_of_recommended_nutrition(cereal, sex):
    """Creates and displays a bar chart over the percentage of a cereal's 
    nutritional content compared to the recommended daily intake
    (protein, carbohydrates, fiber, fat, salt)
    
    Parameters:
    cereal: Cereal object
    sex: String - either 'Male' or 'Female'. Sex needed for recommended daily nutritional intake
    """
    data = __get_recommended_nutrition()
    df = data[data[:]['Sex'] == sex.capitalize()]
    recommended = __get_recommended_nutrition_from_dataframe(df)
    actual = cereal.nutrition.get_nutrition_as_list()
    pcts = [(ac / rec) * 100 for ac, rec in zip(actual, recommended)]
    labels = 'Calories', 'Protein', '  Carbohydrates', 'Fiber', 'Fat', 'Salt'
    title = "Percentage of %s %s's Nutrional Content compared to Daily Recommended Intake" % (cereal.brand.capitalize(),
                                                                                              cereal.name.capitalize())
    __plot_percentage(pcts, labels, title) 

def __plot_prices_in_store(cereals_prices, title):
    names = cereals_prices.keys()
    prices = cereals_prices.values()
    plt.bar(names, prices, width=0.5, align='center')
    plt.xticks(rotation=15, horizontalalignment='right',fontweight='light')
    plt.ylabel('Price in DKK', fontsize=10)
    plt.grid(axis='y', color='grey')
    plt.title(title)
    plt.show()
    
def __plot_percentage(pcts, labels, title):
    plt.bar(labels, pcts, width=0.5, align='center')
    plt.ylabel('Percentage (%)', fontsize=10)
    plt.grid(axis='y', color='grey')
    plt.title(title)
    plt.show()
    
def __get_stores(cereals):
    return list(set([key for cereal in cereals for key in cereal.price.keys()]))

def __get_price(price, grams, per_100g):
    if per_100g:
        return (price/1000) * grams
    return price/10

def __get_nutrition_data(cereals):
    names = [cereal.get_brand_name() for cereal in cereals]
    calories = [str(cereal.nutrition.calories) + ' kcal' for cereal in cereals]
    proteins = [str(cereal.nutrition.protein) + ' g' for cereal in cereals]
    carbs = [str(cereal.nutrition.carbohydrates) + ' g' for cereal in cereals]
    fibers = [str(cereal.nutrition.fiber) + ' g' for cereal in cereals]
    fats = [str(cereal.nutrition.fat) + ' g' for cereal in cereals]
    salts = [str(cereal.nutrition.salt) + ' g' for cereal in cereals]
    return {'Cereal Name': names, 'Calories': calories, 'Protein': proteins, 'Carbohydrates': carbs, 
                                                        'Fiber': fibers, 'Fat': fats, 'Salt': salts}

def __get_recommended_nutrition():
    return pd.read_csv('files/daily_nutrition.csv')

def __get_recommended_nutrition_from_dataframe(df):
    calories = int(df.loc[:,'Calories'].str.replace(' kcal', ''))
    protein = float(df.loc[:,'Protein'].str.replace(' g', ''))
    carbs = float(df.loc[:,'Carbohydrates'].str.replace(' g', ''))
    fiber = float(df.loc[:,'Fiber'].str.replace(' g', ''))
    fat = float(df.loc[:,'Fat'].str.replace(' g', ''))
    salt = float(df.loc[:,'Salt'].str.replace(' g', ''))
    return [calories, protein, carbs, fiber, fat, salt]

def __create_title(store, per_100g):
    if per_100g:
        return 'Cereal Prices per 100 grams at ' + store.capitalize()
    return 'Cereal Prices per at ' + store.capitalize()