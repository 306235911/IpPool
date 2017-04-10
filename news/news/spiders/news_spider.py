# -*- coding: UTF-8 -*-
import scrapy
import re
import mysql
import testmail
from scrapy.mail import MailSender
from scrapy import signals
import testmail


#用于删除所爬文字中带有的html符号的类
class Tool:
    #编译标记了图片及七个空格以及没有图片的情况的正则表达式
    removingImg = re.compile('<img.*?>| {7}|')
    #去链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #去段标签
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    
    def replace(self,x):
        #sub为替换函数
        x = re.sub(self.removingImg , "" , x)
        x = re.sub(self.removeAddr, "" , x)
        x = re.sub(self.replaceLine,"\n" , x)
        x = re.sub(self.replaceTD , "\t" , x)
        x = re.sub(self.replacePara , "\n  ",x)
        x = re.sub(self.replaceBR , "\n" , x)
        x = re.sub(self.removeExtraTag , "" , x)
        # strip可用于把句子前后的空白去掉
        return x.strip()


class NewsSpider(scrapy.Spider):
    mysql = mysql.Mysql()
    tool = Tool()
    name = "news"
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            # 'Host': "news.sina.com.cn",
            "Upgrade-Insecure-Requests": '1',
            # 'Referer': "https://www.baidu.com",
            }
    XinLangid = 0
    WangYiid = 0
    TengXunid = 0
    newsid = 0
    sendmail = testmail.SendMail()

    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NewsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    def spider_closed(self, spider):
        print 'here'
        self.sendmail.sending()
    
    def start_requests(self):
        # AllPro = self.mysql.selectData()
        # print AllPro[0][1]
        # print '111111111111111111111111111111111111111111'
        # print AllPro[0][1]
        urls = [
            'https://www.douban.com/',
        ]
        XinLangUrl = 'http://news.sina.com.cn'
        WangYiUrl = 'http://news.163.com/'
        TengXunUrl = 'http://news.qq.com/'
        self.mysql.clear('new')
        # for url in urls:
        self.headers['host'] = 'news.sina.com.cn'
        yield scrapy.Request(url=XinLangUrl, headers=self.headers, callback=self.XinLang_parse, dont_filter = True)
        self.headers['host'] = 'news.163.com'
        yield scrapy.Request(url=WangYiUrl, headers=self.headers, callback=self.WangYi_parse, dont_filter = True)
        self.headers['host'] = 'news.qq.com'
        yield scrapy.Request(url=TengXunUrl, headers=self.headers, callback=self.TengXun_parse, dont_filter = True)
        
        
        # finally:
        #     self.mailer.send(to=["306235911@qq.com"], subject="title", body="Some body", cc=["daxiong306235911@sina.com"])
        # finally:
        #     if (self.XinLangid == 1 and self.WangYiid == 1 and self.TengXunid == 1):
        #         self.sendmail.sending()
        # # 手动设置成功
        # for url in urls:
        #     yield scrapy.Request(url=url, meta={'proxy': AllPro[0][1]}, headers=self.headers, callback=self.parse)

        # 尝试用下载中间件
    
    # done!    
    def XinLang_parse(self, response):
        # 这里爬的是有带url 的， 可以一起放数据库
        # content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ConsTi", " " ))]//a').extract()
        content = response.xpath('//*[(@id = "all_list_01")]//a').extract()
        for title in content:
            # print title.encode('utf-8').decode('utf-8')
            pattern1 = re.compile('href="(.+?)"', re.S)
            pattern2 = re.compile('/em>(.+?)</a>', re.S)
            NewUrl = re.findall(pattern1, title)
            # print NewUrl[0]
            NewTitle = re.findall(pattern2, title)
            # print ''.join(NewTitle).encode('utf-8').decode('utf-8')
            # print NewTitle[0]
            # print NewUrl[0]
            self.mysql.insertData('new', self.newsid, ''.join(NewTitle)+u'   (新浪)', NewUrl[0].encode('utf-8').decode('utf-8'))
            self.XinLangid = 1
            self.newsid += 1
            
            # print title.encode('utf-8').decode('utf-8')
            # print '\n'
        if response.body:
            print 'Xinlang'
        
    def WangYi_parse(self, response):
        # 也有url
        # content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "red", " " ))]//a').extract()
        content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mod_hot_rank", " " ))]//li//a').extract()
        for title in content:
            pattern1 = re.compile('href="(.+?)"', re.S)
            pattern2 = re.compile('>(.+?)</a>', re.S)
            NewUrl = re.findall(pattern1, title)
            NewTitle = re.findall(pattern2, title)
            # print NewTitle[0]
            # print NewUrl[0]
            self.mysql.insertData('new', self.newsid, NewTitle[0]+u'   (网易)', NewUrl[0].encode('utf-8').decode('utf-8'))
            self.WangYiid = 1
            self.newsid += 1
            
            # print title.encode('utf-8').decode('utf-8')
            # print '\n'
        if response.body:
            print 'WangYi'
            
    def TengXun_parse(self, response):
        # 也是有url的
        # content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "linkto", " " ))]').extract()
        content = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sb", " " ))]//a').extract()
        for title in content:
            pattern1 = re.compile('href="(.+?)"', re.S)
            pattern2 = re.compile('>(.+?)</a>', re.S)
            NewUrl = re.findall(pattern1, title)
            NewTitle = re.findall(pattern2, title)
            # print NewTitle[0]
            # print NewUrl[0]
            self.mysql.insertData('new', self.newsid, NewTitle[0]+u'   (腾讯)', NewUrl[0].encode('utf-8').decode('utf-8'))
            self.TengXunid = 1
            self.newsid += 1
            
            # print title.encode('utf-8').decode('utf-8')
            # print '\n'
        if response.body:
            print 'TengXun'