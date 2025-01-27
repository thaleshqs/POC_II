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
import re
import random

class NBCScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        #self.url = 'https://www.nbcnews.com/politics/2024-presidential-election'
        self.url = 'https://www.nbcnews.com/politics'
        self.outlet = 'nbc'
        
    def scrape(self):
        headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        links = soup.find_all('a')
        articles_set = set()
        
        pattern = re.compile('https:\/\/www\.nbcnews\.com\/(news|politics)\/[^\/]+\/[^\/]+-rcna\d+')
        for link in links:
            href = link.get('href')
            if href and pattern.search(href):
                articles_set.add(href)
        
        
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
            #print(20*'-')
            time.sleep(2)
            headers = {
                "User-Agent": random.choice(self.user_agents)
            }
            response = requests.get(article_url, timeout=15, headers=headers)
          
            #print(article_url)
            #response = requests.get(article_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup)
            try:
                article_published_time = soup.find('time')['datetime']
            except Exception as e:
                continue
                
            date_elements = article_published_time.split('-')
            #print(date_elements)
            
            year = date_elements[0]
            month = date_elements[1]
            day = date_elements[2][:2]

            assert len(year) == 4, 'year should have 4 digits: yyyy'
            assert len(month) == 2, 'month should have 2 digits: mm'
            assert len(day) == 2, 'day should have 2 digits: dd'

            article_published_date = '-'.join([year,month,day])
            #print(article_published_date)

            article_data = NewsPlease.from_url(article_url)
            article_dict = article_data.get_dict()

            
            parsed_url = urlparse(article_url)
            path_segments = parsed_url.path.split('/')
            title_segment = path_segments[-1]
            title_words = title_segment.split('-')
            first_three_words = '-'.join(title_words[:3])

            article_id = '-'.join([self.outlet, article_published_date, first_three_words])
            title = soup.find('h1').text    
            #print(article_id)
            #print(title)
            #print(article_dict['maintext'][:100])
            #print(path_segments)
            

            id_list.append(article_id)
            description_list.append(article_dict['description'])
            title_list.append(title)
            image_url_list.append(article_dict['image_url'])
            main_text_list.append(article_dict['maintext'])
            authors_list.append(article_dict['authors'])
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

            
                        