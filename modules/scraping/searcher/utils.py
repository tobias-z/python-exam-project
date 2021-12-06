def make_float(danish_number: str) -> float:
    return float(danish_number.replace(",", "."))


def remove_chars(number_with_string: str) -> str:
    return number_with_string.replace(" g", "")
