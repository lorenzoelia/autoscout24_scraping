from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class MileagePriceRegression:
    def __init__(self, mileage_values, average_price_values):
        self.mileage_values = mileage_values
        self.average_price_values = average_price_values

    def perform_regression(self, degree=2):
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(self.mileage_values.values.reshape(-1, 1))
        poly_reg = LinearRegression()
        poly_reg.fit(X_poly, self.average_price_values)
        predicted_prices = poly_reg.predict(X_poly)

        return self.mileage_values, predicted_prices
