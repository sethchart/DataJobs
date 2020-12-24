import requests
import time
from bs4 import BeautifulSoup
from fake_headers import Headers
from numpy import random
from JobsDb import JobsDb

class Scraper(object):

    def __init__(self):
        self.db = JobsDb()
        self.header_generator = Headder()

    def get_page(url, params=None):
        headers = self.header_generator.generate()
        page = requests.get(url, params=params, headers=headers).content
        return page

    def get_search_page(page_number=1):
        params = {
            'l': 'USA',
            'sort': 'date',
            'p': page_number
        }
        url = 'https://www.careerjet.com/search/jobs'
        page = self.get_page(url, params=params)
        return page

    def get_jobs_from_page(page):
        soup = BeautifulSoup(page, 'html.parser')
        jobs = soup.find_all('article', class_='job clicky')
        return jobs

    def get_link_from_job(job):
        raw_link = job.find('h2').find('a', href=True)
        url = 'https://www.careerjet.com'+raw_link['href']
        title = raw_link['title']
        link = {
            'url': url,
            'title': title
        }
        return link

    def get_description(url):
        """Given a url for a careerjet job listing. This function will
        scrape the full job description from the page.
        """
        wait_time = random.rand(1)
        time.sleep(wait_time)
        page = self.get_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        description = soup.find('section', class_='content').text
        return description

    def scrape_search_page(page_number=1):
        page = self.get_search_page(page_number=page_number)
        jobs = self.get_jobs_from_page(page)
        for job in jobs:
            try:
                link = get_link_from_job(job)
                title = link['title']
                url = link['url']
                description = self.get_description(url)
                job_dict = {
                    'title': title,
                    'url': url,
                    'description': description
                }
                self.db.write_row_to_table(table_name='jobs', row_dict=job_dict)
            except:
                continue

    def scrape_site(number_of_pages=self.number_of_pages):
        for page_number in range(1, number_of_pages+1):
            scrape_search_page(page_number=page_number)
