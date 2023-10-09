import time
import pandas as pd
from selenium import webdriver


class AutoScout24Scraper:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.base_url = "https://www.autoscout24.it/lst/{}/{}?atype=C&cy=I&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU"
        self.listing_frame = pd.DataFrame(
            columns=["make", "model", "mileage", "fuel-type", "first-registration", "price"])
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--ignore-certificate-errors")
        self.browser = webdriver.Chrome(options=self.options)

    def generate_urls(self, num_pages):
        url_list = [self.base_url.format(self.make, self.model)]
        for i in range(2, num_pages + 1):
            url_to_add = self.base_url.format(self.make,
                                              self.model) + f"&page={i}&search_id=meyjiwlhtq&sort=standard&source=listpage_pagination&ustate=N%2CU"
            url_list.append(url_to_add)
        return url_list

    def scrape(self, num_pages, verbose=False):
        url_list = self.generate_urls(num_pages)

        for webpage in url_list:
            self.browser.get(webpage)
            listings = self.browser.find_elements("xpath", "//article[contains(@class, 'cldt-summary-full-item')]")

            for listing in listings:
                data_make = listing.get_attribute("data-make")
                data_model = listing.get_attribute("data-model")
                data_mileage = listing.get_attribute("data-mileage")
                data_fuel_type = listing.get_attribute("data-fuel-type")
                data_first_registration = listing.get_attribute("data-first-registration")
                data_price = listing.get_attribute("data-price")

                listing_data = {
                    "make": data_make,
                    "model": data_model,
                    "mileage": data_mileage,
                    "fuel-type": data_fuel_type,
                    "first-registration": data_first_registration,
                    "price": data_price
                }

                if verbose:
                    print(listing_data)

                frame = pd.DataFrame(listing_data, index=[0])
                self.listing_frame = self.listing_frame._append(frame, ignore_index=True)
                time.sleep(1)

    def save_to_csv(self, filename="listings.csv"):
        self.listing_frame.to_csv(filename, index=False)

    def quit_browser(self):
        self.browser.quit()
