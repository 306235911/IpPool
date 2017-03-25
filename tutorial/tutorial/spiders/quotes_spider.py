# -*- coding:utf-8 -*-
import scrapy

# scrapy 范例

class QuotesSpider(scrapy.Spider):
    # 在命令行调用爬虫时使用的名字
    name = "quotes"
    # scrapy所要爬的url
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        # alist = []
        # 定义要写入的文件名
        filename = "zhihu.txt"
        # 在文件打开的状态下进行以下操作
        with open(filename, 'wb') as f:
            # 使用xpath找到quote所在的每个div
            for quote in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "quote", " " ))]'):
                # 文件写入。其中xpath表达式的前面的  .  是表明要找的是在已经找到了的div下的子项，而不是在全文中查找
                # 使用 .re() 可以返回一个unicode编码的列表，使用encode来用utf-8解码，使用 ''.join() 来把字符串列表转为字符串，以便使用write写入文件
                f.write(''.join(quote.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "text", " " ))]/text()').re(r'.+?')).encode('utf-8'))
                f.write('\r\n')
                f.write(''.join(quote.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').re(r'.+?')).encode('utf-8'))
                f.write('\r\n')
                f.write(''.join(quote.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "tag", " " ))]/text()').re(r'.+?')).encode('utf-8'))
                f.write('\r\n\r\n\r\n')
                # f.write("%s , %s , %s" % (str(text).decode('utf-8') , str(author).decode('utf-8'), str(tags).decode('utf-8')))
            # for i in alist:
            #     for j in i:
            #         f.write(j.encode('utf-8'))
            # for i in alist:
            #     f.write(''.join(i).encode('utf-8'))
            # alist.append(text)
            # alist.append(author)
            # alist.append(tags)
        # with open(filename, 'wb') as f:
        #     for i in alist:
        #         f.write(i.encode('gbk'))