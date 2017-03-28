# -*- coding: UTF-8 -*-
import scrapy
import json
import re
import urllib
import sys
import mysql

# 该爬虫用于爬取ip代理网站里的ip和端口

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


class PoolSpider(scrapy.Spider):
    identity = 0
    tool = Tool()
    mysql = mysql.Mysql()
    name = "pool"
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.xicidaili.com",
            "Upgrade-Insecure-Requests": '1',
            'Referer': "http://www.xicidaili.com/nn/1",
            }
    
    def start_requests(self):
        urls = 'http://www.xicidaili.com/nn/'
        choice = raw_input('(T)est (C)heck (R)un\n')
        if choice == 'T':
            # fp = open('usefulIp.txt' , 'a')
            # fp.write('')
            # fp.close()
            self.mysql.clearnUsefulIp()
            return self.test()
        elif choice == 'R':
            return self.choice()
        elif choice == 'C':
            return self.check()
        else:
            print 'Wrong input'
        # for i in range(1,11):
        #     print i
        #     yield scrapy.Request(url=urls + str(i), headers=self.headers, callback=self.parse)
    
    def choice(self):
        urls = 'http://www.xicidaili.com/nn/'
        # urls = 'http://www.kuaidaili.com/proxylist/1/'
        self.mysql.clearnIp()
        for i in range(1,11):
            print i
            yield scrapy.Request(url=urls + str(i), headers=self.headers, callback=self.parse)
        
    def parse(self, response):
        
        # good
        ip = response.xpath('//td[(((count(preceding-sibling::*) + 1) = 3) and parent::*)] | //td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]').extract()
        ips = []
        for i in ip:
            ips.append(self.tool.replace(i))
            
        # identity = 0
        if ip:
            while ips != []:
                port = ips.pop()
                Anip = ips.pop()
                if self.mysql.insertData(self.identity, Anip, port):
                    pass
                    # print u"保存ip成功"
                else:
                    print u"保存ip失败"
                self.identity += 1
        
        # filename = 'ipPool.txt'
        # with open(filename, 'w') as f:
        #     count = 1
        #     for eachIp in ips:
        #         f.write(eachIp),
        #         # f.write('\t')
        #         if count%2 == 0:
        #             f.write('\n')
        #         else:
        #             f.write('\t')
        #         count += 1
        #         
        # 以上为把爬到的ip写入文件中
    
    def test(self):
        self.mysql.clearnUsefulIp()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.baidu.com",
            "Upgrade-Insecure-Requests": '1',
            # 'Referer': "http://www.xicidaili.com/nn/1",
            }
        url = 'https://www.baidu.com/'
        
        # fp = open('ipPool.txt' , 'r')
        # AnIp = fp.readlines()
        # fp.close()
        
        AllIp = self.mysql.selectData()
        
        proxys = []
        for p in AllIp:
            # TheIp = p.strip('\n').split('\t')
            # # print TheIp[0],TheIp[1]
            pro = 'http://' + str(p[1]) + ':' + str(p[2])
            try:
                print pro
                yield scrapy.Request(url=url, headers=headers, meta = {'proxy' : pro, 'download_timeout': 10} ,callback=self.test_parse ,dont_filter = True)
            except:
                print 'next'
        # sys.exit(1)
        # 以下为尝试并把能用的ip代理写入一个新的文件
    #     
    def test_parse(self, response):
        print '6666666666666666'
        # fp = open('usefulIp.txt' , 'a')
        # fp.write(response.meta['proxy'])
        # fp.write('\n')
        # print response.meta['proxy']
        proxy = response.meta['proxy']
        if self.mysql.usefulIp(self.identity, proxy):
            pass
            # print u"保存ip成功"
        else:
            print u"保存ip失败"
        self.identity += 1
    
    def check(self):
        url = 'https://www.baidu.com/'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.baidu.com",
            "Upgrade-Insecure-Requests": '1',
            # 'Referer': "http://www.xicidaili.com/nn/1",
            }
        UsefulIp = self.mysql.selectip()
        for eachIp in UsefulIp:
            pro = eachIp[1]
            print pro
            try:
                yield scrapy.Request(url=url, headers=headers, meta = {'proxy' : pro} ,callback=self.check_parse ,dont_filter = True)
            except:
                pass
                identity = eachIp[0]
                self.mysql.delete(identity)
                
            
    def check_parse(self, response):
        print response.meta['proxy']
        print 'OK'
        