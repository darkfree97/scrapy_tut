from scrapy import Spider
from scrapy_splash import SplashRequest


class JsSpider(Spider):
    name = 'dynamic'
    start_urls = ['https://www.coindesk.com/price/ethereum/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        for q in response.css("section.global-content"):
            print(q)