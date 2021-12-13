from IPython.display import display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show_cereal_prices(cereals, title="Cereal Prices"):
    """Creates and displays a bar chart over cereal prices
    
    Parameters:
    cereals: List of Cereal objects
    title: String. Title of the bar chart. Default 'Cereal Prices'
    """
    stores = __get_stores(cereals)
    prices_in_stores = __get_prices_with_cereal_name(stores, cereals)
    names = __get_cereal_names(cereals)
    __plot_prices(names, prices_in_stores, title)
    
def show_prices_per_100g(cereals, title="Cereal Prices per 100 grams"):
    """Creates and displays a bar chart over cereal prices per 100 grams
    
    Parameters:
    cereals: List of Cereal objects
    title: String. Title of the bar chart. Default 'Cereal Prices per 100 grams'
    """
    stores = __get_stores(cereals)
    prices_in_stores = __get_prices_with_cereal_name(stores, cereals, True)
    names = __get_cereal_names(cereals)
    __plot_prices(names, prices_in_stores, title)
    
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
    
def __plot_prices(names, prices_in_stores, title):
    stores = [key for key in prices_in_stores.keys()] 
    prices = __get_prices_without_cereal_name(prices_in_stores)
    
    x_axis = np.arange(len(names))
    width = 0.3
    column_widths = [0 + (width*idx) for idx in x_axis]
    for idx in x_axis:
        plt.bar(x_axis + column_widths[idx], prices[idx], width, label=stores[idx]) 
    plt.ylabel('Price in DKK', fontsize=10)
    plt.grid(axis='y', color='grey')
    plt.xticks(x_axis, names, rotation=15, horizontalalignment='right',fontweight='light')
    plt.title(title)
    plt.legend()
    plt.show()
    
def __plot_percentage(pcts, labels, title):
    plt.bar(labels, pcts, width=0.5, align='center')
    plt.ylabel('Percentage (%)', fontsize=10)
    plt.grid(axis='y', color='grey')
    plt.title(title)
    plt.show()

def __get_cereal_names(cereals):
    return [cereal.brand + " " + cereal.name for cereal in cereals]

def __get_stores(cereals):
    return set([key for cereal in cereals for key in cereal.price.keys()])

def __get_prices_with_cereal_name(stores, cereals, per_100g=False):
    prices_in_stores = {store: {} for store in stores}
    for cereal in cereals:
        for key, value in cereal.price.items():
            if not per_100g:
                prices_in_stores[key].update({cereal.brand + " " + cereal.name: value})
            elif per_100g:
                prices_in_stores[key].update({cereal.brand + " " + cereal.name: (value/cereal.grams)*100})
    return prices_in_stores

def __get_prices_without_cereal_name(prices_with_names):
    prices = []
    for value in prices_with_names.values():
        temp = [price for price in value.values()]
        prices.append(temp)
    return prices

def __get_nutrition_data(cereals):
    names = __get_cereal_names(cereals)
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