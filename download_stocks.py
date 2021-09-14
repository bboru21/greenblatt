import os
from simple_settings import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import datetime
import pandas

CHROMEDRIVER_PATH = '%s/chromedriver' % os.path.dirname(
    os.path.realpath(__file__)
)

if settings.MIN_MARKET_CAP:
    MIN_MARKET_CAP = settings.MIN_MARKET_CAP
else:
    MIN_MARKET_CAP = random.randint(50, 100)

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

    stocks = {}

    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all('tr')

    for row in rows:
        columns = row.find_all('td')

        cursor = 0
        for column in columns:
            column_name = COLUMN_NAMES[cursor]

            if column_name not in stocks:
                stocks[column_name] = []
            stocks[column_name].append(column.text.strip())
            cursor = cursor+1

    return stocks


def write_to_csv(stocks):

    df = pandas.DataFrame.from_dict(stocks)

    usn_urls = []
    yahoo_urls = []
    for value in df['ticker']:
        ticker = value.lower()
        usn_urls.append(f'https://money.usnews.com/investing/stocks/{ticker}/')
        yahoo_urls.append(f'https://finance.yahoo.com/quote/{ticker}')

    df['us_news_url'] = usn_urls
    df['yahoo_url'] = yahoo_urls

    filename = 'mfi_%s_min-market-cap-%s.csv' % (
        datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S'),
        MIN_MARKET_CAP
    )

    if not os.path.exists('csv'):
        os.makedirs('csv')

    df.to_csv(f'{settings.BASE_DIR}/csv/{filename}')

    return filename


html = get_stock_table_html()
stocks = parse_markup(html)
filename = write_to_csv(stocks)

print('stocks downloaded as csv/%s' % filename)
