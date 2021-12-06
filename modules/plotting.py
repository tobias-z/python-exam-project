import matplotlib.pyplot as plt

def get_price_per_100g(cereals):
    return {cereal.brand + " " + cereal.name: (cereal.price/cereal.grams)*100 for cereal in cereals}

def plot_prices(names, prices, title="Cereal prices"):
    plt.bar(names, prices, width=0.5, align='center')
    plt.xticks(rotation=45, horizontalalignment='right',fontweight='light')
    plt.title(title)
    plt.show()

def show_cereal_prices(cereals):
    names = [cereal.brand + " " + cereal.name for cereal in cereals]
    prices = [cereal.price for cereal in cereals]
    plot_prices(names, prices)

def show_prices_per_100g(cereals):
    cereals_dict = get_price_per_100g(cereals)
    names = cereals_dict.keys()
    prices = cereals_dict.values()
    plot_prices(names, prices, title="Cereal prices per 100 grams")