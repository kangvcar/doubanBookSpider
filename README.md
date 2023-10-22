# 豆瓣图书爬虫项目

## 项目描述
该项目是一个基于Scrapy框架的豆瓣图书爬虫，用于爬取豆瓣图书TOP250的图书信息以及这些图书的评论信息。爬虫分为两个部分：

1. **豆瓣图书信息爬虫 (`douban_book_spider`)**: 爬取豆瓣图书TOP250的图书的基本信息，并保存到`output/book_info.csv`文件中。同时，将图书的ID保存到`output/book_ids.txt`文件中。
2. **豆瓣图书评论爬虫 (`douban_book_comment`)**: 根据图书ID爬取对应图书的所有评论信息，并保存到`output/book_comments.csv`文件中。

## 环境要求

- Python 3.6+
- Scrapy 2.0+

## 项目结构
```
douban_book/
│   scrapy.cfg
│   README.md
│   requirements.txt
│
├───douban_book/
│   │   items.py
│   │   middlewares.py
│   │   pipelines.py
│   │   settings.py
│   │   __init__.py
│   │
│   └───spiders/
│           book_comment_spider.py
│           book_spider.py
│           __init__.py
│
└───output/
        book_comments.csv
        book_ids.txt
        book_info.csv
```

## 如何使用

### 安装依赖
首先，确保你已经安装了Python和Scrapy。然后，运行以下命令来安装所需的依赖：

```bash
pip install -r requirements.txt
```

### 运行爬虫

1. 运行豆瓣图书信息爬虫：

```bash
scrapy crawl douban_book_spider
```

该命令会爬取豆瓣图书TOP250的图书信息，并将结果保存到`output/book_info.csv`文件中。同时，图书的ID会被保存到`output/book_ids.txt`文件中。

2. 运行豆瓣图书评论爬虫：

```bash
scrapy crawl douban_book_comment
```

该命令会根据`output/book_ids.txt`文件中的图书ID，爬取这些图书的所有评论信息，并将结果保存到`output/book_comments.csv`文件中。

## 输出文件说明

- `book_info.csv`: 保存了豆瓣图书TOP250的图书基本信息。包含的字段有：
  - `book_id`: 图书ID
  - `title`: 图书标题
  - `cover_link`: 封面链接
  - `is_try_read`: 是否可试读
  - `author`: 作者
  - `publisher`: 出版社
  - `publish_date`: 出版日期
  - `price`: 价格
  - `rating`: 评分
  - `rating_count`: 评分人数

- `book_ids.txt`: 保存了豆瓣图书TOP250的图书ID。

- `book_comments.csv`: 保存了根据图书ID爬取的所有评论信息。包含的字段有：
  - `book_id`: 图书ID
  - `book_name`: 图书标题
  - `username`: 用户名
  - `rating`: 评分
  - `comment_time`: 评论时间
  - `useful_count`: 有用数量
  - `content`: 评论内容

## 注意事项

- 请遵守豆瓣的爬虫使用协议，不要对豆瓣的服务器造成过大的压力。
- 请确保在运行爬虫前，你有足够的磁盘空间来保存爬取的数据。
- 项目中的代码仅供学习和研究目的使用，请勿用于任何商业用途。

---

🎉 祝你使用愉快！ 🎉