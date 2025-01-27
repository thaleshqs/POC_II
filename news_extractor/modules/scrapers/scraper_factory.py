from .base_scraper import BaseScraper
from .cnn_scraper import CNNScraper
from .fox_scraper import FoxScraper
from .abc_scraper import ABCScraper
from .cbs_scraper import CBSScraper
from .apnews_scraper import APNewsScraper
from .vox_scraper import VoxScraper
from .nbc_scraper import NBCScraper
from .newsmax_scraper import NewsmaxScraper
from .nypost_scraper import NYPostScraper
from .newsweek_scraper import NewsweekScraper

SCRAPERS = {
    'cnn': CNNScraper,
    'fox': FoxScraper,
    'abc': ABCScraper,
    'cbs': CBSScraper,
    'apnews': APNewsScraper,
    'vox': VoxScraper,
    'nbc': NBCScraper,
    'newsmax': NewsmaxScraper,
    'nypost': NYPostScraper,
    'newsweek': NewsweekScraper
}

def get_scraper(outlet):
    scraper = SCRAPERS.get(outlet.lower())
    if scraper:
        return scraper()
    else:
        return None
        
        
def get_all_scrapers():
    return [scraper() for scraper in SCRAPERS.values()]