from simple_settings import settings
import pandas
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.scraper.spiders.usnews_spider import USNewsSpider

parser = argparse.ArgumentParser(
    description='Reads Magic Formula Investing Sheet, Scrapes sites for data',
)
parser.add_argument(
    '--input_filename',
    type=str,
    help='name of csv file to read',
)
parser.add_argument(
    '--from_cache',
    action='store_true',
    help='parse downloaded html files instead of making requests',
)

args, unknown = parser.parse_known_args()
input_filename = args.input_filename
from_cache = args.from_cache


CACHE_PATH = settings.BASE_DIR / 'scraper' / 'scraper' / 'spiders' / 'html'

df = pandas.read_csv(
    f'csv/{input_filename}',
    header=0,
)
df = df.dropna()  # drop first empty row

start_urls = []

for index, row in df.iterrows():
    ticker = row['ticker'].lower()

    p = CACHE_PATH / f'usnews-{ticker}.html'

    if from_cache and p.exists():
        start_urls.append(f'file://{p}')
    else:
        start_urls.append(
            f'https://money.usnews.com/investing/stocks/{ticker}/'
        )

process = CrawlerProcess(get_project_settings())
process.crawl(USNewsSpider, start_urls=start_urls, from_cache=from_cache)
process.start()
