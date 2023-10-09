import numpy as np
import matplotlib.pyplot as plt


class MileagePricePlotter:
    def __init__(self, mileage_values, average_price_values, std_deviation_values):
        self.mileage_values = mileage_values
        self.average_price_values = average_price_values
        self.std_deviation_values = std_deviation_values

    def plot_mileage_price(self, predicted_prices_sorted, degree):
        sorted_indices = np.argsort(self.mileage_values)
        mileage_values_sorted = self.mileage_values.iloc[sorted_indices]

        plt.figure(figsize=(10, 6))
        plt.scatter(self.mileage_values, self.average_price_values, marker='o', label='Data Points')
        plt.fill_between(self.mileage_values, self.average_price_values - self.std_deviation_values,
                         self.average_price_values + self.std_deviation_values, alpha=0.2, label='Standard Deviation')
        plt.plot(mileage_values_sorted, predicted_prices_sorted, color='red', label=f'Polynomial Regression (Degree {degree})')
        plt.title('Mileage vs. Price with Polynomial Regression')
        plt.xlabel('Mileage (rounded to thousands)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()