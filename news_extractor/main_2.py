import argparse
from modules.scrapers.scraper_factory import get_scraper, get_all_scrapers
from modules.database import update_database_with_duplicates

def parse_arguments():
    parser = argparse.ArgumentParser(description='News Extractor Script')
    parser.add_argument('outlets', nargs='*', default=None, help='outlet to be used')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if len(args.outlets) == 0:
        scrapers = get_all_scrapers()
    else:
        scrapers = [get_scraper(outlet) for outlet in args.outlets if get_scraper(outlet)]
        

    for scraper in scrapers:
        article_set = scraper.scrape()
        df = scraper.get_dataframe_from_articles(article_set, duplicates=True)
        #print(df)
        update_database_with_duplicates(df)
        
        
        

if __name__ == "__main__":
    main()
        