# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'

lua_script = '''
-- This function emulate loading of page and scrolling to end of a page
-- to load dynamic content for parsing.

function main(splash)
        local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        assert(splash:go(splash.args.url))
        splash:wait(splash.args.wait)

        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end
        splash:wait(splash.args.wait)       
        return splash:html()
end
'''


class GoodsSpider(scrapy.Spider):
    name = 'goods'
    start_urls = [
        'https://rozetka.com.ua/search/?text=',
        # 'https://allo.ua/ua/catalogsearch/result/?q=',
        # 'https://mta.ua/search?description=true&query=',
    ]

    def __init__(self, query='', **kwargs):
        self.start_urls = [url + query for url in self.start_urls]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': lua_script,
                    'wait': 0.5,
                }
            )

    def parse(self, response):
        for item in response.css('div.g-i-tile-l div.g-i-tile:not([class*="preloader-trigger"])'):
            yield {
                'picture': item.css('div.g-i-tile-i-image a img::attr(src)').get(),
                'text': item.css('div.g-i-tile-i-title a::text').get()
            }
