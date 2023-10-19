import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.model_selection import KFold


class MileagePriceRegression:
    def __init__(self, mileage_values, average_price_values, std_deviation_values):
        self.mileage_values = mileage_values
        self.average_price_values = average_price_values
        self.std_deviation_values = std_deviation_values

    def do_regression(self, plot=True):
        degrees, rss_scores = self._evaluate_degrees(degrees=range(1, 5))
        if plot:
            self._plot_rss(degrees, rss_scores)
        best_degree = self._select_best_degree(degrees, rss_scores)
        poly_features, poly_reg = self._train_regression(self.mileage_values, self.average_price_values, best_degree)
        predicted_prices = self._predict(self.mileage_values, poly_features, poly_reg)
        return predicted_prices, best_degree

    def _evaluate_degrees(self, degrees=range(1, 2)):
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

                poly_features, poly_reg = self._train_regression(X_train, y_train, degree)
                y_pred = self._predict(X_test, poly_features, poly_reg)
                rss.append(self._calculate_rss(y_test, y_pred))

            rss_scores.append(np.mean(rss))
        return degrees, rss_scores

    def _predict(self, X_test, poly_features, poly_reg):
        y_pred = poly_reg.predict(poly_features.fit_transform(X_test.values.reshape(-1, 1)))
        return y_pred

    def _train_regression(self, X, y, degree):
        poly_features = PolynomialFeatures(degree=degree)
        poly_reg = LinearRegression()
        poly_reg.fit(poly_features.fit_transform(X.values.reshape(-1, 1)), y)
        return poly_features, poly_reg

    def _select_best_degree(self, degrees, rss_scores, verbose=False):
        # Select the degree with the lowest RSS
        best_degree = degrees[np.argmin(rss_scores)]
        if verbose:
            print(f"The degree that minimizes RSS is {best_degree}")

        return best_degree

    def _calculate_rss(self, y_true, y_pred):
        return np.sum((y_true - y_pred) ** 2)

    def _plot_rss(self, degrees, rss_scores):
        # Plot RSS for each degree
        plt.figure(figsize=(10, 6))
        plt.plot(degrees, rss_scores, marker='o', linestyle='-')
        plt.title('RSS for Different Polynomial Degrees')
        plt.xlabel('Polynomial Degree')
        plt.ylabel('RSS (Mean)')
        plt.grid(True)
        plt.show()

    def plot_mileage_price(self, predicted_prices_sorted, degree):
        sorted_indices = np.argsort(self.mileage_values)
        mileage_values_sorted = self.mileage_values.iloc[sorted_indices]

        plt.figure(figsize=(10, 6))
        plt.scatter(self.mileage_values, self.average_price_values, marker='o', label='Data Points')
        plt.fill_between(self.mileage_values, self.average_price_values - self.std_deviation_values,
                         self.average_price_values + self.std_deviation_values, alpha=0.2, label='Standard Deviation')
        plt.plot(mileage_values_sorted, predicted_prices_sorted, color='red', label=f'Polynomial Regression (Degree {degree})')
        plt.title('Price vs. Mileage with Polynomial Regression')
        plt.xlabel('Mileage (rounded to thousands)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()
