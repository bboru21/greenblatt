import os
import sys

from simple_settings import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import random

import csv
import datetime

CHROMEDRIVER_PATH = '%s/chromedriver' % os.path.dirname(os.path.realpath(__file__))

MIN_MARKET_CAP = settings.MIN_MARKET_CAP if settings.MIN_MARKET_CAP else random.randint(30,100)

COLUMN_NAMES = [
    "company_name",
    "ticker",
    "market_cap",
    "price_from",
    "most_recent_quarter_data",
]

def get_stock_table_html():

    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
    browser.get(('https://www.magicformulainvesting.com/Account/LogOn'))

    username = browser.find_element_by_id('Email')
    username.send_keys(settings.EMAIL)

    password = browser.find_element_by_id('Password')
    password.send_keys(settings.PASSWORD)

    login_button = browser.find_element_by_id('login')
    login_button.click()

    min_market_cap = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'MinimumMarketCap')))
    min_market_cap.clear()
    min_market_cap.send_keys(MIN_MARKET_CAP)

    # get 50 instead of 30 stocks
    stock_numbers = browser.find_elements_by_name('Select30')
    stock_numbers[1].click()

    get_stocks_button = browser.find_element_by_id('stocks')
    get_stocks_button.click()

    stock_table = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'tableform')))

    table_html = stock_table.get_attribute('innerHTML')

    return table_html

def parse_markup(html):

    stocks = []

    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all('tr')
    stocks = []
    for row in rows:
        columns = row.find_all('td')

        stock = {}
        cursor = 0
        for column in columns:
            column_name = COLUMN_NAMES[cursor]
            stock[column_name] = column.text.strip()
            cursor = cursor+1

        stocks.append(stock)

    return stocks

def write_to_csv(stocks):

    file_name = 'mfi_%s_min-market-cap-%s.csv' % ( datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S'), MIN_MARKET_CAP)

    if not os.path.exists('csv'):
        os.makedirs('csv')

    with open('csv/%s' % file_name, mode='w') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        for stock in stocks:
            writer.writerow(stock)

    return file_name

html = get_stock_table_html()
stocks = parse_markup(html)
file_name = write_to_csv(stocks)

print 'stocks downloaded as csv/%s' % file_name