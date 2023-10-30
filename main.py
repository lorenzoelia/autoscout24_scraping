from Miner.AutoScout24Scraper import AutoScout24Scraper
from Analysis.DataProcessor import DataProcessor
from Analysis.MileagePriceRegression import MileagePriceRegression
from Miner.TextFileHandler import TextFileHandler

import os


def main(scrape=False):
    zip_list = where_to_search()
    if scrape:
        scrape_autoscout(zip_list)
    # Data Processing
    data_preprocessed = preprocess()
    # Mileage-Price Regression
    perform_regression(data_preprocessed)


def perform_regression(data_preprocessed):
    grouped_data = data_preprocessed.groupby('mileage_grouped')['price'].agg(['mean', 'std']).reset_index()
    mileage_values = grouped_data['mileage_grouped']
    average_price_values = grouped_data['mean']
    std_deviation_values = grouped_data['std']
    regression = MileagePriceRegression(mileage_values, average_price_values, std_deviation_values)
    predicted_prices, best_degree = regression.do_regression()
    # Mileage-Price Plotting
    regression.plot_mileage_price(predicted_prices, best_degree)


def preprocess():
    processor = DataProcessor(downloaded_listings_file)
    data = processor.read_data()
    data_no_duplicates = processor.remove_duplicates(data)
    data_preprocessed = processor.preprocess_data(data_no_duplicates)
    data_rounded = processor.round(data_preprocessed, 1000)
    processor.save_processed_data(data_rounded, output_file_preprocessed)
    return data_preprocessed


def scrape_autoscout(zip_list):
    scraper = AutoScout24Scraper(make, model, version, year_from, year_to, power_from, power_to, powertype, zip_list,
                                 zipr)
    scraper.scrape(num_pages, True)
    scraper.save_to_csv(downloaded_listings_file)
    scraper.quit_browser()


def where_to_search():
    handler = TextFileHandler(zip_list_file_path)
    handler.load_data_csv()
    zip_list = handler.export_capoluogo_column()
    zip_list = [item.lower() for item in zip_list]
    return zip_list


if __name__ == "__main__":
    make = "audi"
    model = "rs6"
    version = ""
    year_from = "2013"
    year_to = "2018"
    power_from = ""
    power_to = ""
    powertype = "kw"
    num_pages = 20
    zipr = 100

    zip_list_file_path = 'Miner/capoluoghi.csv'
    downloaded_listings_file = f'listings/listings_{make}_{model}.csv'
    output_file_preprocessed = f'listings/listings_{make}_{model}_preprocessed.csv'
    # Create the "listings" folder if it doesn't exist
    if not os.path.exists("listings"):
        os.makedirs("listings")

    main(scrape=True)
