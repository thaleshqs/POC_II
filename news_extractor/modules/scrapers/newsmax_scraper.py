from .base_scraper import BaseScraper
from newsplease import NewsPlease
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil
import time
from urllib.parse import urlparse
import pandas as pd
from tqdm import tqdm
from dateutil import parser
import random

class NewsmaxScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.newsmax.com/politics/'
        self.outlet = 'newsmax'        
        
    def scrape(self):
        #response = requests.get(self.url, headers=self.headers, timeout=10)
        headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        response = requests.get(self.url, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        body = soup.find('div', class_='inside_cover_content')
        article_cards = body.find_all('li', class_='article_link')
        articles_set = set()
        
        
        for card in article_cards:
            href = card.find('a').get('href')
            if href:
                href = 'https://www.newsmax.com' + href
                articles_set.add(href)
                #print(href)
        
        
        return articles_set
    
    
    
    def get_dataframe_from_articles(self, articles_set, duplicates=False):
        id_list = []
        description_list = []
        title_list = []
        image_url_list = []
        main_text_list = []
        authors_list = []
        date_list = []
        url_list = []
        download_times_list = []
        
        before = datetime.fromtimestamp(time.time())
        print(f'Processing for {self.outlet}...')
        for article_url in tqdm(articles_set):
            #print(article_url)
            time.sleep(1)
            response = requests.get(article_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_published_time = soup.find('meta', property='article:published_time')
            if article_published_time is None:
                continue
            date_elements = article_published_time['content'].split('-')

            year = date_elements[0]
            month = date_elements[1]
            day = date_elements[2][:2]

            assert len(year) == 4, 'year should have 4 digits: yyyy'
            assert len(month) == 2, 'month should have 2 digits: mm'
            assert len(day) == 2, 'day should have 2 digits: dd'

            article_published_date = '-'.join([year,month,day])

            

            
            parsed_url = urlparse(article_url)
            path_segments = parsed_url.path.split('/')
            #print(path_segments)
            title_segment = path_segments[-7]
            #print(title_segment)
            title_words = title_segment.split('-')
            first_three_words = '-'.join(title_words[:3])

            article_id = '-'.join([self.outlet, article_published_date, first_three_words])
            title = soup.find('h1').text
            author = soup.find('span', itemprop='author')
            if author is not None:
                author = author.get_text(strip=True)
            image_url = soup.find('meta', property='og:image')['content']
            article_div = soup.find('div', {'id':'mainArticleDiv'})
            maintext = ' '.join([p.get_text() for p in article_div.find_all('p')])
            description = soup.find('meta', property='og:description').get("content", None)
            if description is None:
                description = soup.find('meta', attrs={"name" : "description"}).get("content", None)

            #print(article_id)
            #print(title)
            #print(maintext[:100])
            #print(author)
            

            id_list.append(article_id)
            description_list.append(description)
            title_list.append(title)
            image_url_list.append(image_url)
            main_text_list.append(maintext)
            authors_list.append(author)
            date_list.append(article_published_date)
            url_list.append(article_url)
            
            timestamp = datetime.now().strftime('%Y_%m_%d_%H%M')
            download_times_list.append(timestamp)
               
                
        if duplicates is True:
            df = pd.DataFrame(
                list(zip(id_list, title_list, description_list, date_list, main_text_list, authors_list, url_list, image_url_list, download_times_list)),
                columns = [
                "ID",
                "Title", 
                "Description", 
                "Publication Date", 
                "Main Text", 
                "Authors",  
                "Source URL",
                "Image URL",
                "Download Time"]
                )
        else:
            df = pd.DataFrame(
                list(zip(id_list, title_list, description_list, date_list, main_text_list, authors_list, url_list, image_url_list)),
                columns = [
                "ID",
                "Title", 
                "Description", 
                "Publication Date", 
                "Main Text", 
                "Authors",  
                "Source URL",
                "Image URL"]
                )

            
        print(f'{len(df)} articles found for {self.outlet}')
        after = datetime.fromtimestamp(time.time())
        delta = dateutil.relativedelta.relativedelta(after, before)
        print(f'Processed in {delta.minutes} min {delta.seconds} s')

        return df

            
                        