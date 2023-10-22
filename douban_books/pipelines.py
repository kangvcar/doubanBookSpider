# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
from douban_books.items import DoubanBookCommentItem

if not os.path.exists('output'):
    os.makedirs('output')


class SaveBookIDPipeline:
    def open_spider(self, spider):
        # 当爬虫启动时打开文件
        self.file = open('output/book_ids.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        # 当爬虫关闭时关闭文件
        self.file.close()

    def process_item(self, item, spider):
        # 提取书籍 ID
        book_id = item['book_id']
        # 将书籍 ID 写入文件
        self.file.write(book_id + '\n')
        return item


class CsvExporterPipeline:
    def open_spider(self, spider):
        self.file = open('output/book.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['标题', '封面', '是否可试读', '作者', '出版社', '发行日期', '参考定价', '评分', '评价人数'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([item['title'], item['cover_link'], item['is_try_read'], item['author'], item['publisher'], item['publish_date'], item['price'], item['rating'], item['rating_count']])
        return item


class DoubanBookCommentCsvPipeline:
    def open_spider(self, spider):
        self.file = open('output/book_comment.csv', 'w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['book_id', 'book_name', 'username', 'rating', 'comment_time', 'useful_count', 'content'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, DoubanBookCommentItem):
            self.writer.writerow([item['book_id'], item['book_name'], item['username'], item['rating'], item['comment_time'], item['useful_count'], item['content']])
        return item
