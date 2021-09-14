import re
import scrapy
from simple_settings import settings

filepath = settings.BASE_DIR / 'scraper' / 'scraper' / 'spiders' / 'html'

class USNewsSpider(scrapy.Spider):
    name = "usnews"
    from_cache = False

    def __init__(self, *args, **kwargs):
        self.from_cache = kwargs.get('from_cache', False)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=settings.USNEWS_HEADERS
            )

    def parse(self, response):

        if self.from_cache:
            self.log(f'from_cache passed, no file written')
        else:
            urlname = response.url.split("/")[-1]

            pattern = re.compile(r'^(?P<ticker>[a-z]+)-')
            m = re.match(pattern, urlname)
            ticker = m.group('ticker')

            filename = f'usnews-{ticker}.html'
            with open(f'{filepath}/{filename}', 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')