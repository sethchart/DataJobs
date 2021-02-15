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


class Driver():
    """Driver. Wraps interactions with careerjet.com through the selenium
    web driver.
    """

    def __init__(self, location: str = 'USA', search_term: str = 'data'):
        """__init__. Opens a new browser with the first page of careerjet
        search results. Then, clicks on the first job posting. Once this method
        has run, the Driver object is ready to scrape the first job listing.

        Parameters
        ----------
        location : str
            location is a search parameter that allows for regional filtering.
            (default: USA)
        search_term : str
            search_term is a search term for our job posting search.
            (default: data)
        """
        self.browser = None
        self.browser = webdriver.Chrome()
        self.browser.get(f'https://www.careerjet.com/search/jobs?l={location}&s={search_term}')
        first_job_listing = self.browser.find_element_by_class_name('job')
        first_job_link = first_job_listing.find_element_by_tag_name('a')
        first_job_link.click()

    def scrape_page(self) -> dict:
        """scrape_page. Scrapes the current job posting and returns a
        dictionary containing job title, job description, and url.

        Parameters
        ----------

        Returns
        -------
        dict
            page_data contains a dictionary containing the job title, job
            description and url from the current job posting.

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
            soup BeautifulSoup object containing the contents of the current
            job posting page. Takes output from _get_current_page_soup.

        Returns
        -------
        str
            tile is the job title form the current job posting.
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
            soup, BeautifulSoup object containing the contents of the current
            job posting page. Takes output from _get_current_page_soup.

        Returns
        -------
        str
            description is the full job description from the current job
            posting.
        """
        description = soup.find('section', class_='content').text
        return description

    def _get_current_page_soup(self) -> BeautifulSoup:
        """_get_current_page_soup. Extracts html source code for current job
        posting and returns BeautifulSoup object for further manipulation.

        Parameters
        ----------

        Returns
        -------
        BeautifulSoup
            soup is the BeautifulSoup object containing the contents of the
            current job posting.
        """
        page = self.browser.page_source
        soup = BeautifulSoup(page, 'html.parser')
        return soup
