# -*- coding: UTF-8 -*-
import scrapy
import mysql

class DoubanSpider(scrapy.Spider):
    mysql = mysql.Mysql()
    name = "douban"
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            'Host': "www.douban.com",
            "Upgrade-Insecure-Requests": '1',
            'Referer': "https://www.douban.com",
            }

    def start_requests(self):
        # AllPro = self.mysql.selectData()
        # print AllPro[0][1]
        # print '111111111111111111111111111111111111111111'
        # print AllPro[0][1]
        urls = [
            'https://www.douban.com/',
        ]
        url = 'https://www.douban.com/'
        # for url in urls:
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter = True)

        # # 手动设置成功
        # for url in urls:
        #     yield scrapy.Request(url=url, meta={'proxy': AllPro[0][1]}, headers=self.headers, callback=self.parse)

        # 尝试用下载中间件
        
    def parse(self, response):
        print response.body