import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


input_file = 'listings.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Remove duplicates based on the specified columns
# You can specify the columns you want to consider when identifying duplicates
# In this case, we're considering all columns except 'price' for duplicate identification
columns_to_check_duplicates = ['make', 'model', 'mileage', 'fuel-type', 'first-registration']
df_no_duplicates = df.drop_duplicates(subset=columns_to_check_duplicates, keep='first')

# Save the cleaned data to a new CSV file without including the index column
output_file = 'listings_no_duplicates.csv'
df_no_duplicates.to_csv(output_file, index=False)

print("Duplicates removed and saved to", output_file)

# Replace 'unknown' mileage with 0 for rows where 'first-registration' is 'new'
df_no_duplicates.loc[df['first-registration'] == 'new', 'mileage'] = 0

# Drop rows where 'first-registration' is not 'new' and mileage is unknown
df_preprocessed = df_no_duplicates.drop(df_no_duplicates[(df_no_duplicates['first-registration'] != 'new') & (df_no_duplicates['mileage'] == 'unknown')].index)

# Reset the index after dropping rows
df_preprocessed = df_preprocessed.reset_index(drop=True)

# Save the modified DataFrame to a new CSV file
output_file = 'listings_preprocessed.csv'
df_preprocessed.to_csv(output_file, index=False)

print("Modified data saved to", output_file)

# Convert 'mileage' column to integers
df_preprocessed['mileage'] = df_preprocessed['mileage'].astype(int)

# Round and group mileage values by thousands
df_preprocessed['mileage_grouped'] = (df_preprocessed['mileage'] // 1000) * 1000

# Group data by mileage and calculate the average price and standard deviation for each group
grouped_data = df_preprocessed.groupby('mileage_grouped')['price'].agg(['mean', 'std']).reset_index()

# Extract mileage, average price, and standard deviation values
mileage_values = grouped_data['mileage_grouped']
average_price_values = grouped_data['mean']
std_deviation_values = grouped_data['std']

# Perform polynomial regression
degree = 2  # Change this degree as needed
poly_features = PolynomialFeatures(degree=degree)
X_poly = poly_features.fit_transform(mileage_values.values.reshape(-1, 1))
poly_reg = LinearRegression()
poly_reg.fit(X_poly, average_price_values)

# Predict prices using the polynomial regression model
predicted_prices = poly_reg.predict(X_poly)

# Sort the data for plotting
sorted_indices = np.argsort(mileage_values)
mileage_values_sorted = mileage_values.iloc[sorted_indices]
predicted_prices_sorted = predicted_prices[sorted_indices]

# Create the 2D plot with polynomial regression curve
plt.figure(figsize=(10, 6))
plt.scatter(mileage_values, average_price_values, marker='o', label='Data Points')
plt.fill_between(mileage_values, average_price_values - std_deviation_values, average_price_values + std_deviation_values, alpha=0.2, label='Standard Deviation')
plt.plot(mileage_values_sorted, predicted_prices_sorted, color='red', label=f'Polynomial Regression (Degree {degree})')
plt.title('Mileage vs. Price with Polynomial Regression')
plt.xlabel('Mileage (rounded to thousands)')
plt.ylabel('Price')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
