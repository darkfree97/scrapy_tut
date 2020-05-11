import scrapy


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    start_urls = [
        'https://twitter.com/marvel',
        'https://twitter.com/dccomics',
    ]

    def parse(self, response):
        for tweet in response.css('div#timeline div.tweet'):
            item = {
                'id': tweet.css('::attr(data-tweet-id)').get(),
                'author': {
                    'id': tweet.css('a.account-group::attr(data-user-id)').get(),
                    'full_name': tweet.css('strong.fullname::text').get(),
                    'href': 'https://twitter.com' + tweet.css('a.account-group::attr(href)').get()
                },
                'text': ''.join(tweet.css('p.tweet-text::text, p.tweet-text s::text, p.tweet-text b::text').getall()),
                'links': (
                    tweet.css('a.twitter-timeline-link::attr(data-expanded-url), '
                              'div.js-macaw-cards-iframe-container::attr(data-card-url)').getall()
                )
            }
            inner_request = self.parse_tweet_iframe(tweet, item)
            yield inner_request

    @staticmethod
    def parse_tweet_iframe(tweet, parent_item):
        url = tweet.css('div.js-media-container .js-macaw-cards-iframe-container::attr(data-full-card-iframe-url)').get()

        if not url:
            return parent_item

        def iframe_parser(response):
            item = response.meta['item']
            item['links'] += response.css('a::attr(href)').getall()
            yield item

        request = scrapy.Request('https://twitter.com{url}'.format(url=url), iframe_parser)
        request.meta['item'] = parent_item
        return request
