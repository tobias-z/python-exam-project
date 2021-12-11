import itertools
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from modules.scraping.cereal import Cereal
from modules.scraping.searcher.foetex import get_foetex_page
from modules.scraping.searcher.irma import get_irma_page
from modules.scraping.searcher.nemlig import get_nemlig_page


def get_cereal(cereal: Tuple[str, str]) -> List[Cereal]:
    """Finds a single cerial"""
    name, brand = cereal
    name = name.lower()

    # get_nemlig_page
    callbacks = [get_foetex_page, get_irma_page]

    def get_website(cb) -> List[Cereal]:
        # Send brand aswell to add is_original propterty
        return cb(name)

    with ThreadPoolExecutor(len(callbacks)) as ex:
        res = ex.map(get_website, callbacks)

    ## put all similar items together price = {"føtex": 10, "nemlig": 20}

    return [*res.__next__(), *res.__next__()]


def get_cereals(*cereals: Tuple[str, str]):
    """Finds each cereal in parallel"""
    with ThreadPoolExecutor(len(cereals)) as ex:
        res = ex.map(get_cereal, cereals)

    return list(itertools.chain(*res))


if __name__ == "__main__":
    c = get_cereals(("Cornflakes", "Kellogg's"), ("Musli", "Something"))
    print(len(c))
    for cereal in c:
        print(
            cereal.name,
            cereal.brand,
            cereal.grams,
            cereal.price,
            cereal.nutrition.fat,
            cereal.nutrition.protein,
            cereal.nutrition.carbohydrates,
            cereal.nutrition.fiber,
            cereal.nutrition.salt,
        )
