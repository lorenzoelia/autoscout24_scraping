# Autoscout24 Scraping and Polynomial Regression Project

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

This project is a Python-based web scraping and data analysis tool designed to collect vehicle listings from the Autoscout24 website. It aims to perform polynomial regression on the average prices of vehicles, binned by thousands of miles, and select the best polynomial degree using k-fold cross-validation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [License](#license)

## Overview

Autoscout24 is a popular platform for buying and selling vehicles. This project allows you to gather vehicle listings and perform polynomial regression analysis on the average prices, categorized by mileage. By scraping Autoscout24's web pages, extracting metadata, and running regression analysis, you can gain insights into how mileage affects vehicle prices.

## Features

- Web scraping of Autoscout24 listings.
- Extraction of metadata from the HTML web code.
- Polynomial regression analysis on average prices.
- Selection of the best polynomial degree via k-fold cross-validation.

## Requirements

Before using this project, ensure you have the following dependencies installed:

- Python 3.x
- Libraries in `requirements.txt`

To install the required libraries, you can run the following command:

```shell
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine:

```shell
git clone https://github.com/lorenzoelia/autoscout24_scraping.git
```

2. Navigate to the project directory:

```shell
cd autoscout24_scraping
```

3. Create the `listings` folder (if it doesn't already exist):

```shell
mkdir listings
```

4. Run the Python script to perform the scraping and polynomial regression:

```shell
python main.py
```

5. The script will collect listings, preprocess the data, run regression analysis, and select the best polynomial degree.

6. The results will be saved to files within the `listings` folder.

7. Review the generated CSV files for listings and processed data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[MIT License](https://opensource.org/licenses/MIT)
