import scrapy


class BaseballscraperItem(scrapy.Item):
    year = scrapy.Field()
    prefecture = scrapy.Field()
    shortName = scrapy.Field()
    fullName = scrapy.Field()
    regionalBest = scrapy.Field()
    nationalBest = scrapy.Field()
