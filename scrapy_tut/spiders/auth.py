import scrapy
from scrapy.utils.response import open_in_browser


class AuthTestSpider(scrapy.Spider):
    name = 'auth'
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        token = response.css('form input[name="csrf_token"]::attr(value)').get()
        return scrapy.FormRequest.from_response(
            response=response,
            formdata={
                'username': 'un',
                'password': 'pw',
                'csrf_token': token
            },
            callback=self.scrap
        )

    def scrap(self, response):
        # open_in_browser(response)
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('//div[@class="text"]/text()')
            }
