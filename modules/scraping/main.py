from typing import List
from concurrent.futures import ThreadPoolExecutor
from modules.cereal import Cereal
from modules.scraping.searcher.foetex import get_foetex_page
from modules.scraping.searcher.irma import get_irma_page
from modules.scraping.searcher.nemlig import get_nemlig_page


def get_cereal(name: str, brand: str) -> List[Cereal]:
    """Finds a single cerial"""
    name = name.lower()

    callbacks = [get_foetex_page, get_irma_page, get_nemlig_page]

    def get_website(cb) -> List[Cereal]:
        return cb(name, brand)

    with ThreadPoolExecutor(len(callbacks)) as ex:
        res = ex.map(get_website, callbacks)

    cereal_list = [*next(res), *next(res), *next(res)]

    result = []
    for cereal in cereal_list:
        for inner_c in cereal_list:
            if cereal.name + cereal.brand == inner_c.name + inner_c.brand:
                cereal.price = {**cereal.price, **inner_c.price}

        result.append(cereal)

    return result


if __name__ == "__main__":
    c = get_cereal("Musli", "Kellogg's")
    print(len(c))
    for ce in c:
        print(
            ce.name,
            ce.brand,
            ce.grams,
            ce.price,
            ce.nutrition.fat,
            ce.nutrition.protein,
            ce.nutrition.carbohydrates,
            ce.nutrition.fiber,
            ce.nutrition.salt,
        )
