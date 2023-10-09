from AutoScout24Scraper import AutoScout24Scraper

if __name__ == "__main__":
    make = "mercedes-benz"
    model = "a-250"
    num_pages = 20

    scraper = AutoScout24Scraper(make, model)
    scraper.scrape(num_pages)
    scraper.save_to_csv()
    scraper.quit_browser()
