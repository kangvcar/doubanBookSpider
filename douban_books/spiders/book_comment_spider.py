import scrapy
import json
from douban_books.items import DoubanBookCommentItem


class DoubanBookCommentSpider(scrapy.Spider):
    name = 'douban_book_comment'

    # Step 1: Generate start_urls from music_ids.txt
    with open('output/book_ids.txt', 'r') as f:
        book_ids = [line.strip() for line in f.readlines()]
    print(book_ids)
    # Step 2: Generate start_urls from book.csv
    start_urls = [f'https://book.douban.com/subject/{book_id}/' for book_id in book_ids]

    def parse(self, response):
        self.logger.info(f"Parsing: {response.url}")

        # Extract music name
        book_title = response.css('h1 span::text').get()
        print(book_title)

        # Construct the initial comments URL
        book_id = response.url.split("/")[4]
        comments_url = f'https://book.douban.com/subject/{book_id}/comments/?start=0&limit=20&status=P&sort=new_score&comments_only=1'
        print(comments_url)
        yield scrapy.Request(url=comments_url, callback=self.parse_comments, meta={'book_title': book_title, 'book_id': book_id})

    def parse_comments(self, response):
        # Extract the HTML content from the JSON data
        html_content = response.json()['html']
        selector = scrapy.Selector(text=html_content)
        book_name = response.meta['book_title']
        book_id = response.meta['book_id']

        data = json.loads(response.text)

        # 解析评论
        for comment in selector.css('li.comment-item'):
            item = DoubanBookCommentItem()
            item['book_id'] = book_id
            item['book_name'] = book_name
            item['username'] = comment.css('a::attr(title)').get()
            item['rating'] = comment.css('.comment-info span.rating::attr(title)').get()
            # rating_class = comment.css('span.rating::attr(class)').get()
            # item['rating'] = self.parse_rating(rating_class) if rating_class else None
            item['comment_time'] = comment.css('span.comment-info > a.comment-time::text').get()

            # item['comment_time'] = comment.css('span.comment-time::text').get()
            item['useful_count'] = comment.css('span.vote-count::text').get()
            item['content'] = comment.css('span.short::text').get()
            yield item

        # 处理分页
        # start = int(response.url.split('start=')[1].split('&')[0])
        # if data['has_next']:
        #     next_start = start + 20
        #     next_url = f'https://book.douban.com/subject/{book_id}/comments/?start={next_start}&limit=20&status=P&sort=score&comments_only=1'
        #     yield scrapy.Request(next_url, callback=self.parse, meta={'book_id': book_id})

        # Handle pagination
        # Step 2: Update the base_url construction
        book_id = response.url.split("/")[4]
        base_url = f"https://book.douban.com/subject/{book_id}/comments/"
        next_page = selector.css('#paginator a[data-page="next"]::attr(href)').get()
        if next_page:
            next_page_url = base_url + next_page + '&comments_only=1'
            yield scrapy.Request(url=next_page_url, callback=self.parse_comments, meta={'book_title': book_name, 'book_id': book_id})
