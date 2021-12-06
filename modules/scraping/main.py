from typing import List
#from exam_project.modules.scraping.cereal import Cereal
from searcher.foetex import get_foetex_page
from searcher.irma import get_irma_page
from searcher.nemlig import get_nemlig_page

def get_cerial(name: str, brand: str) -> List[Cereal]:
    cerials: List[Cereal] = list()
    foetex = get_foetex_page(name)
    irma = get_irma_page(name)
    nemlig = get_nemlig_page(name)

    # find alle produkter fra alle siderne

    # find ud af hvilke af dem er orignale

    return cerials


if __name__ == "__main__":
    get_cerial("Cornflakes", "Kellogs")
