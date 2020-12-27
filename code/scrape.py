from careerjet import Scraper

def main():
    scraper = Scraper(number_of_pages=5)
    scraper.scrape_site()
    scraper.db.close()

main()

