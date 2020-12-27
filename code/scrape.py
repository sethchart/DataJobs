from careerjet import Scraper
from JobsDb import JobsDb
from timeit import default_timer
from time import sleep
from numpy.random import rand

def main(number_of_pages=2):
    db = JobsDb()
    scraper = Scraper()
    for page in range(number_of_pages):
        start_time = default_timer()
        sleep(rand(1))
        page_data = scraper.scrape_page()
        try:
            db.write_row_to_table('jobs', page_data)
        except:
            print(page_data)
            continue
        scraper.next_page()
        elapsed = default_timer() - start_time
        print(
            f'Scraped page {page+1} of {number_of_pages} pages in {elapsed} seconds'
        )
    db.close()
    scraper.browser.close()

number_of_pages = int(input('How many pages would you like to scrape? '))
main(number_of_pages=number_of_pages)

