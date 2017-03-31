# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql
#设置服务器所需信息
#163邮箱服务器地址
class SendMail():
    def ready(self):
        self.mysql = mysql.Mysql()
        with open('abc.html','w') as f:
            AllNews = self.mysql.selectData('new')
        
            for n in AllNews:
                title = n[1].encode('utf-8')
                url = n[2].encode('utf-8')
                content = '<a href="%s">%s</a><br><br>' % (url, title)
                # print content
                f.write(content)
    
    def sending(self):
        mail_host = 'smtp.sina.com'  
        #163用户名
        mail_user = 'daxiong306235911@sina.com'  
        #密码(部分邮箱为授权码)
        password = raw_input('password:\n')
        # mail_pass = '7a6q5p10q'
        mail_pass = password
        #邮件发送方邮箱地址
        sender = 'daxiong306235911@sina.com'  
        #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        # receivers = ['306235911@qq.com', ' 591640519@qq.com']
        receivers = ['306235911@qq.com']
        
        ##设置eamil信息
        #添加一个MIMEmultipart类，处理正文及附件
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receivers[0]
        message['Subject'] = u'今日份的新闻'
        #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
        self.ready()
        with open('abc.html','r') as f:
            content = f.read()
        #设置html格式参数
        part1 = MIMEText(content,'html','utf-8')
        message.attach(part1)
        print '2'

        
        #登录并发送
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host,25)
            smtpObj.login(mail_user,mail_pass)
            smtpObj.sendmail(
                sender,receivers,message.as_string())
            print('success')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('error',e)

# class Ha():
#     def hah(self):
#         pass