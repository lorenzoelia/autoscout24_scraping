from AutoScout24Scraper import AutoScout24Scraper
from DataProcessor import DataProcessor
from MileagePricePlotter import MileagePricePlotter
from MileagePriceRegression import MileagePriceRegression
from TextFileHandler import TextFileHandler


def main(scrape=False):
    handler = TextFileHandler(zip_list_file_path)
    handler.load_data_csv()
    zip_list = handler.export_capoluogo_column()
    zip_list = [item.lower() for item in zip_list]
    input_file = f'listings/listings_{make}_{model}.csv'
    if scrape:
        scraper = AutoScout24Scraper(make, model, version, year_from, year_to, power_from, power_to, powertype, zip_list,
                                     zipr)
        scraper.scrape(num_pages, True)
        scraper.save_to_csv(input_file)
        scraper.quit_browser()
    # Data Processing
    output_file_no_duplicates = f'listings/listings_{make}_{model}_no_duplicates.csv'
    output_file_preprocessed = f'listings/listings_{make}_{model}_preprocessed.csv'
    processor = DataProcessor(input_file)
    data = processor.read_data()
    data_no_duplicates = processor.remove_duplicates(data)
    data_preprocessed = processor.preprocess_data(data_no_duplicates)
    data_rounded = processor.round(data_preprocessed, 1000)
    processor.save_processed_data(data_rounded, output_file_preprocessed)
    # Mileage-Price Regression
    grouped_data = data_preprocessed.groupby('mileage_grouped')['price'].agg(['mean', 'std']).reset_index()
    mileage_values = grouped_data['mileage_grouped']
    average_price_values = grouped_data['mean']
    regression = MileagePriceRegression(mileage_values, average_price_values)
    mileage_values, predicted_prices, best_degree = regression.perform_regression()
    # Mileage-Price Plotting
    std_deviation_values = grouped_data['std']
    plotter = MileagePricePlotter(mileage_values, average_price_values, std_deviation_values)
    plotter.plot_mileage_price(predicted_prices, best_degree)


if __name__ == "__main__":
    make = "ford"
    model = "fiesta"
    version = "st"
    year_from = ""
    year_to = ""
    power_from = ""
    power_to = ""
    powertype = "kw"
    num_pages = 10
    zipr = 100

    zip_list_file_path = 'capoluoghi.csv'

    main()
