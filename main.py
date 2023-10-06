import selenium
from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.keys import Keys
import os
import time
import csv
import re

# Install the Chrome WebDriver
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--ignore-certificate-errors")

# Create an instance of the browser
browser = webdriver.Chrome(options=option)

# Specify make and model
make = "mercedes-benz"
model = "a-250"
url = "https://www.autoscout24.it/lst/" + make + "/" + model + "?atype=C&cy=I&desc=0&sort=standard&source" \
                                                               "=homepage_search-mask&ustate=N%2CU"

# Create list of URLs we need to open
i = 2
url_list = [url]

# Iterate in order to create URls
while i < 21:
    url_to_add = "https://www.autoscout24.it/lst/" + make + "/" + model + "?atype=C&cy=I&desc=0&page=" + str(
        i) + "&search_id=meyjiwlhtq&sort=standard&source=listpage_pagination&ustate=N%2CU"
    url_list.append(url_to_add)
    i += 1

# Print the resulting list
print(url_list)

# Create a dataframe
listing_frame = pd.DataFrame(columns=["make", "model", "mileage", "fuel-type", "first-registration", "price"])

# Iterate over the different webpages created previously
for webpage in url_list:
    # Open the webpage
    browser.get(webpage)

    # Use the XPath expression to select the desired element
    listings = browser.find_elements("xpath", "//article[contains(@class, 'cldt-summary-full-item')]")

    # Iterate over the listings in order to find each listing's details
    for listing in listings:
        # Extract the desired attributes
        data_make = listing.get_attribute("data-make")
        data_model = listing.get_attribute("data-model")
        data_mileage = listing.get_attribute("data-mileage")
        data_fuel_type = listing.get_attribute("data-fuel-type")
        data_first_registration = listing.get_attribute("data-first-registration")
        data_price = listing.get_attribute("data-price")

        # Create a dictionary where we'll momentarily store the data
        listing_data = {"make": data_make,
                        "model": data_model,
                        "mileage": data_mileage,
                        "fuel-type": data_fuel_type,
                        "first-registration": data_first_registration,
                        "price": data_price}

        print(listing_data)

        # Add dictionary to a dataframe
        frame = pd.DataFrame(listing_data, index=[0])

        # Append dataframe to main dataframe
        listing_frame = listing_frame._append(frame, ignore_index=True)

        # Wait time
        time.sleep(1)

print(listing_frame)
listing_frame.to_csv("listings.csv")

# Quit the browser
browser.quit()
