# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBooksItem(scrapy.Item):
    book_id = scrapy.Field()
    title = scrapy.Field()
    cover_link = scrapy.Field()
    is_try_read = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    publish_date = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()


class DoubanBookCommentItem(scrapy.Item):
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    username = scrapy.Field()
    rating = scrapy.Field()
    comment_time = scrapy.Field()
    useful_count = scrapy.Field()
    content = scrapy.Field()
