# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import GitHubUser


class GithubGroupSpider(CrawlSpider):
    name = 'github_group'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/darkfree97']

    rules = [
        Rule(LinkExtractor(allow=(r'^\w+\?after=\w+&tab=followers', r'\w+\?tab=followers$',))),
        Rule(LinkExtractor(allow=(r'^[A-Za-z0-9]+',), deny=('\?tab=', '/\w+/\w+', '/login', '/join'), restrict_css=('main div.position-relative',)), callback='parse_user'),
    ]

    def parse(self, response):
        yield self.get_user_from_response(response)
        yield self.next_or_none(response)

    def parse_user(self, response):
        yield self.get_user_from_response(response)
        yield self.next_or_none(response)

    @staticmethod
    def get_user_from_response(response):
        user = GitHubUser()
        user['full_name'] = response.css('h1.vcard-names span.p-name::text').get()
        user['username'] = response.css('h1.vcard-names span.p-nickname::text').get()
        match = re.search(
            r'https://github\.com/(?P<referer>\w+)\?tab=followers',
            str(response.request.headers.get('Referer', ''))
        )
        if match:
            user['followersList'] = [match.group(1)]
        return user

    def next_or_none(self, response):
        try:
            return next(super().parse(response))
        except StopIteration:
            return None
