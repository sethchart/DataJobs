import json
import requests
from careerjet_api import CareerjetAPIClient
from bs4 import BeautifulSoup

class Scraper(CareerjetAPIClient):
    """Provides tools for scraping careerjet.com"""
    
    def __init__(self,
                 keywords = None,
                 location = 'USA',
                 display_url = 'https:/www.example.com',
                 locale_code="en_US", 
                 path_to_secrets='/home/schart/.secrets.json'):
        super().__init__(locale_code=locale_code)
        self.keywords = keywords
        self.location = location
        self.display_url = display_url
        self.path_to_secrets = path_to_secrets
    
    def search(self, page=1):
        """Executes a search on careerjet.com and returns results as json.
        search keywords and location are specified at class instantiation.
        
        Parameters:
        page -- specify what page of the search results to return (default 1)
        
        Returns:
        json formatted contents of the selected page. Results include up to 
        twenty job posting results. 
        """
        with open(self.path_to_secrets) as f:
            affid = json.load(f)['careerjet']['affid']
        search_params = {
            'affid': affid,
            'user_ip': requests.get('https://icanhazip.com').text.strip('\n'),
            'url': self.display_url,
            'user_agent': requests.utils.default_user_agent(),
            'location': self.location,
            'keywords': self.keywords,
            'sort': 'date',
            'page': page
        }
        results = super().search(search_params)
        return results
    
    def _get_full_description(self, url):
        html_page = requests.get(url)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        description = soup.find('section', class_='content').text
        return description
    
    def _append_full_descriptions(self, results):
        jobs = results['jobs']
        for index, job in enumerate(jobs):
            url = job['url']
            full_description = self._get_full_description(url)
            job['full_description'] = full_description
            jobs[index] = job
        results['jobs'] = jobs
        return results
    
    def scrape_page(self, page=1):
        results = self._search(page=page)
        results_with_full_description = self._append_full_descriptions(results)
        return results_with_full_description