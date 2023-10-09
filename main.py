from AutoScout24Scraper import AutoScout24Scraper
from DataProcessor import DataProcessor
from MileagePricePlotter import MileagePricePlotter
from MileagePriceRegression import MileagePriceRegression


if __name__ == "__main__":
    make = "mercedes-benz"
    model = "a-250"
    num_pages = 20

    input_file = f'listings_{make}_{model}.csv'

    # scraper = AutoScout24Scraper(make, model)
    # scraper.scrape(num_pages, True)
    # scraper.save_to_csv(input_file)
    # scraper.quit_browser()

    # Data Processing
    output_file_no_duplicates = 'listings_no_duplicates.csv'
    output_file_preprocessed = 'listings_preprocessed.csv'

    processor = DataProcessor(input_file)
    data = processor.read_data()
    data_no_duplicates = processor.remove_duplicates(data)
    data_preprocessed = processor.preprocess_data(data_no_duplicates)
    data_rounded = processor.round(data_preprocessed, 1000)
    processor.save_processed_data(data_preprocessed, output_file_preprocessed)

    # Mileage-Price Regression
    grouped_data = data_preprocessed.groupby('mileage_grouped')['price'].agg(['mean', 'std']).reset_index()
    mileage_values = grouped_data['mileage_grouped']
    average_price_values = grouped_data['mean']

    regression = MileagePriceRegression(mileage_values, average_price_values)
    degree = 2
    mileage_values, predicted_prices = regression.perform_regression(degree)

    # Mileage-Price Plotting
    std_deviation_values = grouped_data['std']
    plotter = MileagePricePlotter(mileage_values, average_price_values, std_deviation_values)
    plotter.plot_mileage_price(predicted_prices, degree)
