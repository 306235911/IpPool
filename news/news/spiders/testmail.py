# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
import email
from email.mime.multipart import MIMEMultipart
import mysql
#设置服务器所需信息
#163邮箱服务器地址
class SendMail():
    def ready(self):
        self.mysql = mysql.Mysql()
        AllNews = self.mysql.selectData('new')
        content = ''
        for n in AllNews:
            title = n[1].encode('utf-8')
            url = n[2].encode('utf-8')
            each_line = '<a href="%s">%s</a><br><br>' % (url, title)
            content = content + each_line

        sql = "select value from config where field='laoju'"
        laoju = self.mysql.NoemalSelect(sql)
        str_laoju = laoju[0][0].split(",")
        content = content + "<h5>%s<br><br>%s<br><br>%s</h5>" %(str_laoju[0].encode('utf-8'), str_laoju[1].encode('utf-8'), str_laoju[2].encode('utf-8'))

        return content
        # with open('abc.html','w') as f:
        #     AllNews = self.mysql.selectData('new')
        #
        #     for n in AllNews:
        #         title = n[1].encode('utf-8')
        #         url = n[2].encode('utf-8')
        #         content = '<a href="%s">%s</a><br><br>' % (url, title)
        #         # print content
        #         f.write(content)
    
    def sending(self):
        mail_host = 'smtp.sina.com'
        #163用户名
        mail_user = 'daxiong306235911@sina.com'
        #密码(部分邮箱为授权码)
        # password = raw_input('password:\n')
        # mail_pass = 'Ilove,ldm1'
        mail_pass = '7B6A5Z10B'
        # mail_pass = password
        #邮件发送方邮箱地址
        sender = 'daxiong306235911@sina.com'
        #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        # receivers = ['306235911@qq.com', '591640519@qq.com']
        # receivers = ['daxiong306235911@sina.com']
        # receivers = ['daxiong306235911@sina.com']
        receivers = ['zhuyuting0508@sina.com','daxiong306235911@sina.com']

        ##设置eamil信息
        #添加一个MIMEmultipart类，处理正文及附件
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ";".join(receivers)
        # message['To'] = receivers[0]
        # message['CC'] = '306235911@qq.com'
        message['Subject'] = u'新闻推送邮件'
        #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
        # self.ready()
        # with open('abc.html','r') as f:
        #     content = f.read()
        #     # content = f.readline
        # #设置html格式参数
        # print content[:80:]
        # content = '<a href="http://news.163.com/17/0918/10/CUK1KVKQ0001875P.html">aaa'
        content = self.ready()
        part1 = MIMEText(content.replace(".","%2E"),'html','utf-8')
        message.attach(part1)

        
        #登录并发送
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # smtpObj.connect(mail_host,25)
            smtpObj.login(mail_user,mail_pass)
            # for receiver in receivers:
            smtpObj.sendmail(sender,receivers,message.as_string())
            print('success')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('error',e)

# class Ha():
#     def hah(self):
#         pass