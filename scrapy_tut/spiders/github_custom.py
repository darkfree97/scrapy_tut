# -*- coding: utf-8 -*-
import logging

import scrapy

from ..items import GitHubUser


class GithubGroupSpider(scrapy.Spider):
    name = 'github_custom'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/darkfree97']

    def parse(self, response):
        user = self.get_user_from_response(response)
        return self.parse_followers(response, user)

    def parse_nested_user(self, response):
        parent = response.meta['parent']
        user = self.get_user_from_response(response)
        parent['followersList'] = parent.get('followersList', [])
        parent['followersList'] += [dict(user)]
        return parent if response.meta['last'] else self.parse_followers(response, user)

    def parse_nested_follower_links(self, response):
        urls = response.css('a.d-inline-block.no-underline.mb-1::attr(href)')\
                       .re(r'^/(?!join)(?!features)(?!login)\w+')
        for link in urls:
            user_request = scrapy.Request(response.urljoin(link), self.parse_nested_user)
            user_request.meta['parent'] = response.meta['parent']
            user_request.meta['last'] = link == urls[-1]
            yield user_request

        if not urls:
            yield response.meta['parent']

    def parse_followers(self, response, parent):
        links = response.xpath("//a/@href")
        links = links.re(r'^\w+\?after=\w+&tab=followers') or links.re(r'\w+\?tab=followers$')
        request = scrapy.Request(response.urljoin(links[0]), self.parse_nested_follower_links)
        request.meta['parent'] = parent
        return request

    @staticmethod
    def get_user_from_response(response):
        user = GitHubUser()
        user['full_name'] = response.css('h1.vcard-names span.p-name::text').get()
        user['username'] = response.css('h1.vcard-names span.p-nickname::text').get()
        return user
