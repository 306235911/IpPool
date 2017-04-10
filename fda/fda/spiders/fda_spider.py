# -*- coding: UTF-8 -*-

import scrapy

class FdaSpider(scrapy.Spider):
    name = "fda"
    start_urls = [
        "https://www.fda.gov/NewsEvents/Newsroom/PressAnnouncements/default.htm"
    ]

    def parse(self, response):
        content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "panel-body", " " ))]//a').extract()
        print content