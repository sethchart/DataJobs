# ~/usr/bin/env python3
"""This script executes a scrape of job postings from careerjet.com and stores
postings in an sqlite3 database.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

from job_database import JobsDb
from careerjet import Driver
from timeit import default_timer
from time import sleep
from numpy.random import rand


def scrape(num_job_postings: int = 2):
    """scrape. Scrapes the selected number of job postings from careerjet.com.

    Parameters
    ----------
    num_job_postings : int (default: 2)
        num_job_postings is the number of job postings that should be scraped
        during the session.
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
            f'{outcome} scraped page {page+1} of {num_job_postings} pages\
            in {elapsed} seconds'
        )
    db.close()
    driver.browser.close()


if __name__ == "__main__":
    num_job_postings = int(input('How many pages would you like to scrape? '))
    scrape(num_job_postings=num_job_postings)
