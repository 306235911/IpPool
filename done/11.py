# -*- coding: UTF-8 -*-
import scrapy
import json
import re

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


class ZhihuSpider(scrapy.Spider):
    tool = Tool()
    name = "zhihu"
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.zhihu.com",
            "Upgrade-Insecure-Requests": '1',
            'Referer': "http://www.zhihu.com/",
            }
    
    def start_requests(self):
        urls = [
            'https://www.zhihu.com/login/email',
        ]
        parameters = '''/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default'''
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.zhihu.com",
            "Upgrade-Insecure-Requests": '1',
            'Referer': "http://www.zhihu.com/",
    }
        userAgen = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # print url+parameters
        for url in urls:
            # print url+parameters
            yield scrapy.Request(url=url, meta = {'cookiejar' : 1}, headers=headers, callback=self.parse)
            
            
    def parse(self, response):
        xsrf = scrapy.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        url = 'https://www.zhihu.com/login/email'
        
        yield scrapy.FormRequest.from_response(response, url=url, headers = self.headers, meta={'cookiejar': response.meta['cookiejar']}, formdata={'_xsrf': xsrf, 'email': '306235911@qq.com', 'password': '7b6a5z10b'}, callback=self.parse_after)
    
    def parse_after(self, response):
        url = 'https://www.zhihu.com/api/v4/questions/43677446'
        # 下面的offset貌似是从第几个答案开始爬
        parameters = '''/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=30&sort_by=default'''
        yield scrapy.Request(url=url+parameters, meta={'cookiejar': response.meta['cookiejar']}, headers=self.headers, callback=self.last_parse)
        
    def last_parse(self, response):
         # 定义要写入的文件名
        filename = "zhihu.txt"
        # 在文件打开的状态下进行以下操作
        with open(filename, 'w') as f:
            pattern = re.compile("editable_content': u'(.+?)', u'" , re.S)
            questions = json.loads(response.body.decode('utf-8'))
            items = re.findall(pattern , str(questions['data']))
            contents = []
            for item in items:
            # 去掉杂项
                content = "\n" + self.tool.replace(item) + "\n"
            # 以兼容中文的编码规则把帖子内容添加入contents
                contents.append(content.encode('utf-8'))
            for i in contents:
                a = i.decode("unicode-escape")
                f.write(a.encode('utf-8'))
