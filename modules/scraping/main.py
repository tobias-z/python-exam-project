import original_product


def get_cerial(name: str, brand: str):
    original_products = original_product.get_original_products(name, brand)


if __name__ == "__main__":
    get_cerial("Cornflakes", "Kellogs")
