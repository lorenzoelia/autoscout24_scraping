import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.model_selection import KFold


class MileagePriceRegression:
    def __init__(self, mileage_values, average_price_values):
        self.mileage_values = mileage_values
        self.average_price_values = average_price_values

    def perform_regression(self):
        degrees, rss_scores = self.evaluate_degrees(degrees=range(1, 5))
        self.plot_rss(degrees, rss_scores)
        best_degree = self.select_best_degree(degrees, rss_scores)
        x_poly, predicted_prices = self.regression(best_degree)
        return x_poly, predicted_prices, best_degree

    def evaluate_degrees(self, degrees=range(1, 2)):
        # Number of folds for cross-validation
        k = 10
        # Initialize lists to store results
        rss_scores = []
        for degree in degrees:
            X = self.mileage_values
            y = self.average_price_values

            # K-fold cross-validation
            kf = KFold(n_splits=k)
            rss = []

            for train_index, test_index in kf.split(X):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]

                poly_features = PolynomialFeatures(degree=degree)
                poly_reg = LinearRegression()
                poly_reg.fit(poly_features.fit_transform(X_train.values.reshape(-1, 1)), y_train)
                y_pred = poly_reg.predict(poly_features.fit_transform(X_test.values.reshape(-1, 1)))
                rss.append(self.calculate_rss(y_test, y_pred))

            rss_scores.append(np.mean(rss))
        return degrees, rss_scores

    def regression(self, degree):
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(self.mileage_values.values.reshape(-1, 1))
        poly_reg = LinearRegression()
        poly_reg.fit(X_poly, self.average_price_values)
        predicted_prices = poly_reg.predict(X_poly)
        return X_poly, predicted_prices

    def select_best_degree(self, degrees, rss_scores, verbose=False):
        # Select the degree with the lowest RSS
        best_degree = degrees[np.argmin(rss_scores)]
        if verbose:
            print(f"The degree that minimizes RSS is {best_degree}")

        return best_degree

    def calculate_rss(self, y_true, y_pred):
        return np.sum((y_true - y_pred) ** 2)

    def plot_rss(self, degrees, rss_scores):
        # Plot RSS for each degree
        plt.figure(figsize=(10, 6))
        plt.plot(degrees, rss_scores, marker='o', linestyle='-')
        plt.title('RSS for Different Polynomial Degrees')
        plt.xlabel('Polynomial Degree')
        plt.ylabel('RSS (Mean)')
        plt.grid(True)
        plt.show()
