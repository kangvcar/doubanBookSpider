import scrapy
from douban_books.items import DoubanBooksItem
import re


class DoubanBookSpider(scrapy.Spider):
    name = 'douban_book_spider'
    start_urls = ['https://book.douban.com/top250']

    def parse(self, response):
        # 解析书籍信息
        for book_tr in response.css('tr.item'):
            item = DoubanBooksItem()
            # 提取书籍URL
            book_url = book_tr.css('div.pl2 > a::attr(href)').get()
            # 提取书籍ID
            item['book_id'] = book_url.split('/')[-2] if book_url else None

            item['title'] = book_tr.css('div.pl2 a::text').get().strip()
            item['cover_link'] = book_tr.css('td a.nbg img::attr(src)').get()
            item['is_try_read'] = "是" if book_tr.css('div.pl2 img[title="可试读"]') else "否"

            # 提取作者、出版社、发行日期和价格的信息
            details = book_tr.css('p.pl::text').get().strip().split(' / ')
            item['author'] = details[0]
            item['publisher'] = details[-3]
            item['publish_date'] = details[-2]
            item['price'] = details[-1]

            item['rating'] = book_tr.css('span.rating_nums::text').get()
            rating_count_text = book_tr.css('span.pl::text').get()
            item['rating_count'] = re.search(r'(\d+)人评价', rating_count_text).group(1) if rating_count_text else None
            yield item

        # 翻页处理
        next_page = response.css('span.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
