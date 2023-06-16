# Pharmacies Scraping

This project involves web scraping of online pharmacies and stores using Selenium and BeautifulSoup libraries in Python. The goal is to extract product information from different online stores.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- pandas

## Installation

You can install the required libraries using pip:
- pip install selenium beautifulsoup4 pandas webdriver_manager

## Working

- The script uses a pharmacies list stored in data file and load the list of pharmacies from the dataset and initiate a web driver for Chrome.

- The script will attempt to visit each pharmacy's URL using the Selenium driver.

- After visiting the pharmacy's URL, the script will search for products using CSS selectors and extract information such as name, price, and URL.

The extracted product information will be printed in the console.

