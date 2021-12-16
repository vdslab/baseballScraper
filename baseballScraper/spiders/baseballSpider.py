from os import scandir
import scrapy
from baseballScraper.items import BaseballscraperItem


class BaseballspiderSpider(scrapy.Spider):
    name = 'baseballSpider'
    allowed_domains = ['www.hb-nippon.com']
    start_urls = ['https://www.hb-nippon.com']

    def parse(self, response):
        prefectureList = response.css(
            ".prefectureList").css("a")  # 県のリストから県を抽出
        for prefecture in prefectureList:
            prefectureName = prefecture.css("a::text").extract_first()
            print(prefectureName)
            prefectureUrl = response.urljoin(
                prefecture.css("a::attr(href)").extract_first())
            yield scrapy.Request(prefectureUrl, callback=self.parse_detail, cb_kwargs={"prefectureName": prefectureName}, dont_filter=True)

    def parse_detail(self, response, prefectureName):
        separatePrefectures = response.css("#past-results > b::text").extract()
        tables = response.css(".table_normal > tbody")
        if not separatePrefectures:
            separatePrefectures = [prefectureName]
        for separatePrefecture, table in zip(separatePrefectures, tables):
            years = table.css("tr")
            for year in years:
                year, schools = year.css("a::text").extract()[
                    0], year.css("a")[1:]
                cnt = 1
                for school in schools:
                    item = BaseballscraperItem()

                    item["year"] = year
                    item["prefecture"] = separatePrefecture
                    item["shortName"] = school.css("a::text").extract_first()
                    item["regionalBest"] = 1 if cnt <= 1 else (
                        2 if cnt <= 2 else (4 if cnt <= 4 else 8))
                    item["nationalBest"] = None
                    cnt += 1
                    yield scrapy.Request(school.css("a::attr(href)").extract_first(), callback=self.getFullSchollName, meta={"item": item}, dont_filter=True)

    def getFullSchollName(self, response):
        item = response.meta["item"]
        fullName = response.css("#school_info").css("a::text").extract_first()
        item["fullName"] = fullName if fullName else None
        yield item
