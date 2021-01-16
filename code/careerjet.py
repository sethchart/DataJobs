"""
This module provides the Scraper class, which encapsulates interaction with
careerjet.com through the selenium webdriver. It provides the key methods
required for executing a scrape of job postings.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

class Scraper(object):
    """Scraper. Wraps interactions with careerjet.com through the selenium
    webdriver.
    """


    def __init__(self):
        self.browser = None
        self._initialize_scraper()

    def scrape_page(self):
        """Scrapes the current job posting"""
        soup = self._get_current_page_soup()
        page_data = {
            'title': self._get_title(soup),
            'url': self.browser.current_url,
            'description': self._get_description(soup)
        }
        return page_data

    def next_page(self):
        """Advances the browser to the next job posting"""
        nav_bar = self.browser.find_element_by_class_name('nav')
        next_button = nav_bar.find_element_by_class_name('next')
        current_url = self.browser.current_url
        next_button.click()
        wait = WebDriverWait(self.browser, 10)
        wait.until(lambda x: x.current_url != current_url)

    @staticmethod
    def _get_title(soup):
        """Extracts the job title from the current posting"""
        title = soup.find('h1').text
        return title

    @staticmethod
    def _get_description(soup):
        """Extracts the description from the current posting"""
        description = soup.find('section', class_='content').text
        return description

    def _get_current_page_soup(self):
        """Parses the current job posting using BeautifulSoup"""
        page = self.browser.page_source
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def _initialize_scraper(self):
        """Opens a new browser with the first page of creerjet search results.
        Then, clicks on the first job posting. Once this method has run, the
        scraper object is ready to scrape the first job listing.
        """
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.careerjet.com/search/jobs?l=USA&s=data')
        first_job_posting = self.browser.find_element_by_class_name('job')
        first_job_link = first_job_posting.find_element_by_tag_name('a')
        first_job_link.click()
