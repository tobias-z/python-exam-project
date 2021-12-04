from typing import List
from exam_project.modules.scraping.cereal import Cereal
from searcher.foetex import get_foetex_page
from searcher.irma import get_irma_page
from searcher.nemlig import get_nemlig_page
from concurrent.futures import ThreadPoolExecutor


def get_cerial(name: str, brand: str) -> List[Cereal]:
    # get_nemlig_page
    callbacks = [get_foetex_page, get_irma_page]
    name = name.lower()

    def get_website(cb) -> List[Cereal]:
        return cb(name)

    with ThreadPoolExecutor(len(callbacks)) as ex:
        res = ex.map(get_website, callbacks)

    return [*res.__next__(), *res.__next__()]


if __name__ == "__main__":
    cereals = get_cerial("Musli", "Kellogs")
    print(len(cereals))
    for cereal in cereals:
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
