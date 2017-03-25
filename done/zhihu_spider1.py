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
            # 'X-Requested-With': "XMLHttpRequest"
            }
    
    def start_requests(self):
        urls = [
            # 'https://www.zhihu.com/question/43677446',
            'https://www.zhihu.com/login/email',
        ]
        parameters = '''/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=40&sort_by=default'''
        userAgen = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # print url+parameters
        for url in urls:
            # print url+parameters
            yield scrapy.Request(url=url, meta = {'cookiejar' : 1}, headers=self.headers, callback=self.parse)
            
            
    def parse(self, response):
        # parameters = '''/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default'''
        xsrf = scrapy.Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        # url = 'https://www.zhihu.com/api/v4/questions/43677446'
        url = 'https://www.zhihu.com/login/email'
        
        yield scrapy.FormRequest.from_response(response, url=url, headers = self.headers, meta={'cookiejar': response.meta['cookiejar']}, formdata={'_xsrf': xsrf, 'email': '306235911@qq.com', 'password': '7b6a5z10b'}, callback=self.parse_after)

    
    def parse_after(self, response):
        url = 'https://www.zhihu.com/api/v4/questions/43677446'
        # 下面的offset貌似是从第几个答案开始爬
        parameters = '''/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20&sort_by=default'''
        yield scrapy.Request(url=url+parameters, meta={'cookiejar': response.meta['cookiejar']}, headers=self.headers, callback=self.last_parse)
        
    def last_parse(self, response):
         # 定义要写入的文件名
        filename = "zhihu.txt"
        # 在文件打开的状态下进行以下操作
        with open(filename, 'a') as f:
            # 使用xpath找到quote所在的每个div
            # f.write(response.body)
            # questions = response.re(r'"editable_content": "(.+?)"')
            # f.write(''.join(question.encoding('utf-8')))
            # questions = scrapy.Selector(response).re(r'{"editable_content": "(.+?)", "reviewing_comments_count"')
            # questions = scrapy.Selector(response).xpath('//p/text()').re(r'{"editable_content": "(.+)')
            pattern = re.compile("editable_content': u'(.+?)', u'" , re.S)
            # questions = json.loads(response.body, encoding='utf-8')
            questions = json.loads(response.body.decode('utf-8'))
            
            next_url = questions['paging']['next']
            totals = questions['paging']['totals']
            # print totals
            # print next_url
            
            items = re.findall(pattern , str(questions['data']))
            contents = []
            for item in items:
            # 去掉杂项
                content = "\n" + self.tool.replace(item) + "\n"
            # 以兼容中文的编码规则把帖子内容添加入contents
                contents.append(content.encode('utf-8'))
            # print contents
            # f.write(' '.join((contents)).encode('utf-8').decode("unicode-escape").strip())
            
            pattern2 = re.compile("offset=(\d+)" , re.S)
            now_offset = re.search(pattern2 , next_url).group(1).strip()
            print now_offset
            
            for i in contents:
                a = i.decode("unicode-escape")
                f.write(a.encode('utf-8'))
                
        if int(now_offset) < int(totals):
            yield scrapy.Request(next_url, meta={'cookiejar': response.meta['cookiejar']}, headers=self.headers, callback=self.last_parse)
        else:
            print 'done'
                
                # f.write(i.decode("unicode-escape"))
            #     
            # f.write(str(questions['data']))
            
            
            #     print '\n'
            # f.write(''.join(questions).decode('utf-8').encode('utf-8'))
            # print type(''.join(questions.re(r'.+?')))
            # f.write(i for i in questions['data'])
            
        # 此上已经能用    
    
            
            # for question in questions:
                # text = question.xpath('.//p')
                # yield text
            # f.write(''.join(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "UserLink-link", " " ))]').re(r'.+')).encode('utf-8'))
            # for question in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "UserLink-link", " " ))]'):
                # 文件写入。其中xpath表达式的前面的  .  是表明要找的是在已经找到了的div下的子项，而不是在全文中查找
                # 使用 .re() 可以返回一个unicode编码的列表，使用encode来用utf-8解码，使用 ''.join() 来把字符串列表转为字符串，以便使用write写入文件
                # f.write(''.join(question.re(r'.+？')).encode('utf-8'))
                # f.write(''.join(question.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "UserLink-link", " " ))]/text()').re(r'.+?')).encode('utf-8'))
                # f.write('\r\n')
                # f.write(''.join(question.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "Voters", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "Button--plain", " " ))]/text()').re(r'.+?')).encode('utf-8'))
                # f.write('\r\n')
                # f.write(''.join(question.xpath('.//p/text()').re(r'.+?')).encode('utf-8'))
                # f.write('\r\n\r\n\r\n')
                # 
    # def parse(self, response):
    #     filename = 'zhihu.txt'
    #     with open(filename, 'wb') as f:
    #         # f.write(response.xpath('//p/text()').extract())
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

# class ZhihuSpider(scrapy.Spider):
#     name = "zhihu"
#     start_urls = [
#         'https://www.zhihu.com/question/43677446',
#         # 'https://www.zhihu.com/question/45146576',
#     ]
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
#     }
# 
#     def start_requests(self):
#         url = 'https://www.zhihu.com/question/43677446'
#         yield scrapy.Request(url, headers=self.headers)    
# 
#     # def parse(self, response):
#     #         for q in response.css('div.List-item'):
#     #             yield {
#     #                 'text': zhihu.xpath('//p/text()').extract_first(),
#     #             }
#                 
#                 
#     def parse(self, response):
#         filename = 'zhihu.txt'
#         with open(filename, 'wb') as f:
#             for q in response.css('div.List-item'):
#                 text = zhihu.xpath('//p/text()').extract_first()
#                 f.write(text)
    