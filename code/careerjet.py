#!/usr/bin/env python3
"""
This module provides the Driver class, which encapsulates interaction with
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
from timeit import default_timer
from numpy.random import rand
from job_database import JobsDb

class Driver(object):
    """Driver. Wraps interactions with careerjet.com through the selenium
    web driver.
    """

    def __init__(self):
        """__init__. Opens a new browser with the first page of careerjet search results.
        Then, clicks on the first job posting. Once this method has run, the
        Driver object is ready to scrape the first job listing.
        """
        self.browser = None
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.careerjet.com/search/jobs?l=USA&s=data')
        first_job_listing = self.browser.find_element_by_class_name('job')
        first_job_link = first_job_listing.find_element_by_tag_name('a')
        first_job_link.click()

    def scrape_page(self):
        """scrape_page. Scrapes the current job posting and returns a
        dictionary containing job title, job description, and url.
        """
        soup = self._get_current_page_soup()
        page_data = {
            'title': self._get_title(soup),
            'url': self.browser.current_url,
            'description': self._get_description(soup)
        }
        return page_data

    def next_page(self):
        """next_page. Advances the browser to the next job posting.
        """
        nav_bar = self.browser.find_element_by_class_name('nav')
        next_button = nav_bar.find_element_by_class_name('next')
        current_url = self.browser.current_url
        next_button.click()
        wait = WebDriverWait(self.browser, 10)
        wait.until(lambda x: x.current_url != current_url)

    @staticmethod
    def _get_title(soup: BeautifulSoup) -> str:
        """_get_title. Extracts the job title from the current posting.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object containing the contents of the current job
            posting page. Takes output from _get_current_page_soup.
        """
        title = soup.find('h1').text
        return title

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        """_get_description. Extracts the description from the current
        posting.

        Parameters
        ----------
        soup : BeautifulSoup
            BeautifulSoup object containing the contents of the current job
            posting page. Takes output from _get_current_page_soup.
        """
        description = soup.find('section', class_='content').text
        return description

    def _get_current_page_soup(self):
        """_get_current_page_soup. Extracts html source code for current job
        posting and returns BeautifulSoup object for further manipulation.
        """
        page = self.browser.page_source
        soup = BeautifulSoup(page, 'html.parser')
        return soup


def scrape(num_job_postings=2):
    """Summary of scrape. Scrapes `num_job_postings` job postings from
    careerjet.com.

    Parameters
    ----------
    num_job_postings : int (default 2)
        number of job postings to scrape from careerjet.com.
    """
    db = JobsDb()
    driver = Driver()
    for page in range(num_job_postings):
        start_time = default_timer()
        sleep(rand(1))
        page_data = driver.scrape_page()
        try:
            db.write_row_to_table('jobs', page_data)
            outcome = 'Successfully'
        except:
            outcome = 'Unsuccessfully'
        try:
            driver.next_page()
        except:
            print('Unable to get next page.')
            pass
        elapsed = default_timer() - start_time
        print(
            f'{outcome} scraped page {page+1} of {num_job_postings} pages in {elapsed} seconds'
        )
    db.close()
    driver.browser.close()

if __name__ == "__main__":
    num_job_postings = int(input('How many pages would you like to scrape? '))
    scrape(num_job_postings=num_job_postings)
