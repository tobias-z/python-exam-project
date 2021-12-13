from modules.cereal import Cereal


def make_float(danish_number: str) -> float:
    return float(danish_number.replace(",", "."))


def remove_chars(number_with_string: str) -> str:
    return number_with_string.replace(" g", "")


def get_original(cereal: Cereal, search_name: str, brand: str):
    if (
        cereal.name.lower() + cereal.brand.lower()
        == search_name.lower() + brand.lower()
    ):
        cereal.is_original = True
    return cereal
