#!/usr/bin/env python3
"""
This module executes a scrape of the first `number_of_pages` job postings from
careerjet.com and stores them in an SQLite database.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

from careerjet import Scraper
from JobsDb import JobsDb
from timeit import default_timer
from time import sleep
from numpy.random import rand

def main(number_of_pages=2):
    """Summary of main. Scrapes `number_of_pages` job postings from
    careerjet.com.

    Parameters
    ----------
    number_of_pages : int (default 2)
        number of job postings to scrape from careerjet.com.
    """
    db = JobsDb()
    scraper = Scraper()
    for page in range(number_of_pages):
        start_time = default_timer()
        sleep(rand(1))
        page_data = scraper.scrape_page()
        try:
            db.write_row_to_table('jobs', page_data)
            outcome = 'Successfully'
        except:
            outcome = 'Unsuccessfully'
        try:
            scraper.next_page()
        except:
            print('Unable to get next page.')
            pass
        elapsed = default_timer() - start_time
        print(
            f'{outcome} scraped page {page+1} of {number_of_pages} pages in {elapsed} seconds'
        )
    db.close()
    scraper.browser.close()

if __name__ == "__main__":
    number_of_pages = int(input('How many pages would you like to scrape? '))
    main(number_of_pages=number_of_pages)


