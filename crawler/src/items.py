import scrapy


class PageItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    domain = scrapy.Field()
